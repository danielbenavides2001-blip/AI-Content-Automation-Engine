import os
import time
from pathlib import Path
from typing import Optional

import requests
from tools.common.base_model import BaseModelTool
from tools.common.messenger import Messenger


class FacebookTool(BaseModelTool):
    """
    Tool for interacting with Facebook Graph API.
    Handles video uploads (including Reels) and photo posts to a Facebook Page.
    """
    page_id: str
    access_token: str
    api_version: str = "v19.0"

    @property
    def base_url(self) -> str:
        return f"https://graph.facebook.com/{self.api_version}"

    @property
    def video_url(self) -> str:
        return f"https://graph-video.facebook.com/{self.api_version}"

    def upload_video(
        self,
        file_path: Path,
        description: str = "",
        title: Optional[str] = None
    ) -> str:
        """
        Uploads a video to a Facebook Page using the resumable (chunked) upload API.
        """
        if not file_path.exists():
            raise FileNotFoundError(f"Video file not found: {file_path}")

        file_size = file_path.stat().st_size
        chunk_size = 10 * 1024 * 1024  # 10MB per chunk
        
        Messenger.info(f"🚀 Starting Facebook video upload: {file_path.name} ({file_size / (1024*1024):.2f} MB)")

        # 1. START Phase
        params = {
            "upload_phase": "start",
            "file_size": file_size,
            "access_token": self.access_token
        }
        
        response = requests.post(f"{self.video_url}/{self.page_id}/videos", params=params)
        if response.status_code != 200:
            Messenger.error(f"START Phase failed: {response.status_code} - {response.text}")
            response.raise_for_status()
        
        data = response.json()
        
        upload_session_id = data["upload_session_id"]
        video_id = data["video_id"]
        
        Messenger.info(f"   Upload session started: {upload_session_id}")

        # 2. TRANSFER Phase (Chunks)
        with open(file_path, "rb") as f:
            start_offset = 0
            while start_offset < file_size:
                chunk = f.read(chunk_size)
                end_offset = start_offset + len(chunk)
                
                percentage = (start_offset / file_size) * 100
                Messenger.info(f"   Uploading chunk: {start_offset} - {end_offset} ({percentage:.0f}%)")
                
                files = {
                    "video_file_chunk": ("chunk.mp4", chunk, "video/mp4")
                }
                data_payload = {
                    "upload_phase": "transfer",
                    "upload_session_id": upload_session_id,
                    "start_offset": start_offset,
                }
                
                resp = requests.post(
                    f"{self.video_url}/{self.page_id}/videos",
                    params={"access_token": self.access_token},
                    data=data_payload,
                    files=files
                )
                resp.raise_for_status()
                
                start_offset = end_offset

        Messenger.info("   Transfer complete.")

        # 3. FINISH Phase
        finish_params = {
            "upload_phase": "finish",
            "upload_session_id": upload_session_id,
            "description": description,
            "access_token": self.access_token
        }
        if title:
            finish_params["title"] = title

        response = requests.post(f"{self.video_url}/{self.page_id}/videos", params=finish_params)
        response.raise_for_status()
        
        if response.json().get("success"):
            Messenger.success(f"✅ Video published successfully! ID: {video_id}")
            return video_id
        else:
            raise RuntimeError(f"Finish phase failed: {response.text}")

    def upload_photo(self, file_path: Path, caption: str = "") -> str:
        """
        Uploads a photo to the Facebook Page and PUBLISHES it immediately.
        """
        if not file_path.exists():
            raise FileNotFoundError(f"Photo file not found: {file_path}")

        Messenger.info(f"📸 Uploading photo: {file_path.name}")
        
        url = f"{self.base_url}/{self.page_id}/photos"
        files = {"source": open(file_path, "rb")}
        data = {
            "caption": caption,
            "access_token": self.access_token
        }
        
        response = requests.post(url, data=data, files=files)
        response.raise_for_status()
        
        photo_id = response.json().get("id")
        Messenger.success(f"✅ Photo published! ID: {photo_id}")
        return photo_id

    def upload_photo_unpublished(self, file_path: Path) -> str:
        """
        Uploads a photo to Facebook but keeps it UNPUBLISHED.
        Returns the photo ID for use in multi-photo posts.
        """
        if not file_path.exists():
            raise FileNotFoundError(f"Photo file not found: {file_path}")

        url = f"{self.base_url}/{self.page_id}/photos"
        files = {"source": open(file_path, "rb")}
        data = {
            "published": "false",
            "access_token": self.access_token
        }
        
        response = requests.post(url, data=data, files=files)
        response.raise_for_status()
        return response.json().get("id")

    def create_carousel_post(self, description: str, photo_ids: list[str]) -> str:
        """
        Creates a single post with multiple photos (Carousel style).
        """
        Messenger.info(f"📸 Creating carousel post with {len(photo_ids)} photos...")
        
        url = f"{self.base_url}/{self.page_id}/feed"
        
        attached_media = []
        for pid in photo_ids:
            attached_media.append({"media_fbid": pid})

        import json
        data = {
            "message": description,
            "attached_media": json.dumps(attached_media),
            "access_token": self.access_token
        }
        
        response = requests.post(url, data=data)
        response.raise_for_status()
        
        post_id = response.json().get("id")
        Messenger.success(f"✅ Carousel post published! ID: {post_id}")
        return post_id

    def create_text_post(self, message: str) -> str:
        """
        Creates a text-only post on the Facebook Page.
        """
        Messenger.info("📝 Creating text post...")
        
        url = f"{self.base_url}/{self.page_id}/feed"
        data = {
            "message": message,
            "access_token": self.access_token
        }
        
        response = requests.post(url, data=data)
        response.raise_for_status()
        
        post_id = response.json().get("id")
        Messenger.success(f"✅ Text post published! ID: {post_id}")
        return post_id
