
from pathlib import Path
from typing import Any, ClassVar, List, Optional, Type, TypeVar, Union

from pydantic import BaseModel, PrivateAttr

from flows.image_content_generator.pipeline.prompt_base.models import VideoScript
from flows.image_content_generator.pipeline.prompt_longs.manager import PromptManagerLongs
from flows.image_content_generator.pipeline.prompt_shorts.manager import PromptManagerShorts
from flows.image_content_generator.pipeline.schemas import AudioAlignment, State, VideoOrientation
from flows.image_content_generator.pipeline.storage_csv import CsvStore
from tools.audio_generation.audio_tool import AudioTool
from tools.audio_generation.gemini import GeminiAudioGenerator
from tools.audio_generation.vertex_ai_tts import VertexAIAudioGenerator
from tools.common.base_model import BaseModelTool
from tools.common.messenger import Messenger
from tools.image_generation.gemini import GeminiImageGenerator
from tools.image_generation.vertex_ai import VertexAIImageGenerator
from tools.image_generation.midjourney import ImageTask
from tools.text_generation.gemini import GeminiTextGenerator
from tools.utils.text import slugify
from tools.utils.time import retry
from tools.social_media.facebook import FacebookTool
from tools.video_editing.ffmpeg import FFmpegTool
from tools.video_editing.whisper import WhisperTool
from tools.video_editing.remotion import RemotionTool

T = TypeVar("T", bound=BaseModel)
PromptManager = Union[PromptManagerShorts, PromptManagerLongs]


class Pipeline(BaseModelTool):
    """
    Main pipeline for the Image Content Generator project.
    Orchestrates the creation of shorts using AI tools.
    """
    out_base: Path
    resource_base: Path
    orientation: VideoOrientation

    _text_gen: Optional[GeminiTextGenerator] = PrivateAttr(default=None)
    _image_gen: Optional[Union[GeminiImageGenerator, VertexAIImageGenerator]] = PrivateAttr(default=None)
    _audio_gen: Optional[Union[GeminiAudioGenerator, VertexAIAudioGenerator]] = PrivateAttr(default=None)
    _ffmpeg: Optional[FFmpegTool] = PrivateAttr(default=None)
    _whisper: Optional[WhisperTool] = PrivateAttr(default=None)
    _prompt_manager: Optional[PromptManager] = PrivateAttr(default=None)
    _audio_tool: Optional[AudioTool] = PrivateAttr(default=None)
    _store: Optional[CsvStore] = PrivateAttr(default=None)
    _facebook: Optional[FacebookTool] = PrivateAttr(default=None)
    _remotion: Optional[Any] = PrivateAttr(default=None)

    # Standard Output Directories
    IDEAS_DIR: ClassVar[str] = "ideas"
    IMAGES_DIR: ClassVar[str] = "images"
    AUDIOS_DIR: ClassVar[str] = "audios"
    VIDEOS_DIR: ClassVar[str] = "videos"
    EDITIONS_DIR: ClassVar[str] = "editions"
    REMOTION_DIR: ClassVar[str] = "flows/image_content_generator/remotion"

    # Standard Output Files
    IDEA_JSON: ClassVar[str] = "idea.json"
    SCRIPT_JSON: ClassVar[str] = "script.json"
    RAW_VIDEO: ClassVar[str] = "raw_video.mp4"
    SUBTITLED_VIDEO: ClassVar[str] = "subtitled_video.mp4"
    REMOTION_VIDEO: ClassVar[str] = "remotion_frames"
    PRO_SUBTITLED_VIDEO: ClassVar[str] = "pro_subtitled_video.mp4"
    FINAL_AUDIO: ClassVar[str] = "final_audio.wav"
    FINAL_SUBS: ClassVar[str] = "final_subs.srt"
    FINAL_VIDEO: ClassVar[str] = "final_video.mp4"

    # Standard Scene Patterns
    SCENE_IMAGE_PATTERN: ClassVar[str] = "scene_{}.png"
    SCENE_AUDIO_PATTERN: ClassVar[str] = "scene_{}.wav"
    SCENE_VIDEO_PATTERN: ClassVar[str] = "scene_{}.mp4"
    BATCH_AUDIO_PATTERN: ClassVar[str] = "batch_{}.wav"

    # Standard Resource Directories
    BG_MUSIC_DIR: ClassVar[str] = "bg-music"
    REFERENCES_DIR: ClassVar[str] = "reference"

    # Standard Tracking Files
    IDEAS_TRACKING_CSV: ClassVar[str] = "ideas_tracking.csv"

    def __init__(self, **kwargs: Any):
        super().__init__(**kwargs)

    @property
    def store(self) -> CsvStore:
        if self._store is None:
            csv_path = self.out_base / self.IDEAS_TRACKING_CSV
            self._store = CsvStore(csv_path=csv_path)
        return self._store

    @property
    def text_gen(self) -> GeminiTextGenerator:
        if self._text_gen is None:
            self._text_gen = GeminiTextGenerator()
        return self._text_gen

    @property
    def image_gen(self) -> Union[GeminiImageGenerator, VertexAIImageGenerator]:
        if self._image_gen is None:
            import os
            use_vertex = os.getenv("USE_VERTEX_AI_IMAGE", "false").lower() == "true"
            ar_value = "9:16" if self.orientation == VideoOrientation.SHORT else "16:9"
            
            if use_vertex:
                project_id = os.getenv("GCP_PROJECT_ID")
                location = os.getenv("GCP_LOCATION", "us-central1")
                if not project_id:
                    raise ValueError("GCP_PROJECT_ID is required for Vertex AI.")
                self._image_gen = VertexAIImageGenerator(
                    project_id=project_id,
                    location=location,
                    aspect_ratio=ar_value
                )
            else:
                self._image_gen = GeminiImageGenerator(
                    aspect_ratio=ar_value,
                    reference_dir=self.resource_base / self.REFERENCES_DIR,
                )
        return self._image_gen

    @property
    def audio_gen(self) -> Union[GeminiAudioGenerator, VertexAIAudioGenerator]:
        if self._audio_gen is None:
            import os
            use_vertex = os.getenv("USE_VERTEX_AI_AUDIO", "false").lower() == "true"
            if use_vertex:
                self._audio_gen = VertexAIAudioGenerator()
            else:
                self._audio_gen = GeminiAudioGenerator(
                    voice_name=self.prompt_manager.VOICE_NAME
                )
        return self._audio_gen

    @property
    def ffmpeg(self) -> FFmpegTool:
        if self._ffmpeg is None:
            self._ffmpeg = FFmpegTool()
        return self._ffmpeg

    @property
    def whisper(self) -> WhisperTool:
        if self._whisper is None:
            self._whisper = WhisperTool()
        return self._whisper

    @property
    def audio_tool(self) -> AudioTool:
        if self._audio_tool is None:
            bg_music_dir = self.resource_base / self.BG_MUSIC_DIR
            self._audio_tool = AudioTool(bg_music_dir=bg_music_dir)
        return self._audio_tool

    @property
    def prompt_manager(self) -> PromptManager:
        if self._prompt_manager is None:
            if self.orientation == VideoOrientation.SHORT:
                self._prompt_manager = PromptManagerShorts()
            elif self.orientation == VideoOrientation.LONG:
                self._prompt_manager = PromptManagerLongs()
            else:
                raise ValueError(f"Orientation {self.orientation} not supported.")
        return self._prompt_manager

    @property
    def remotion(self) -> RemotionTool:
        if self._remotion is None:
            self._remotion = RemotionTool()
        return self._remotion

    @property
    def facebook(self) -> FacebookTool:
        if self._facebook is None:
            import os
            page_id = os.getenv("FACEBOOK_PAGE_ID")
            access_token = os.getenv("FACEBOOK_PAGE_ACCESS_TOKEN")
            if not page_id or not access_token:
                raise ValueError("FACEBOOK_PAGE_ID and FACEBOOK_PAGE_ACCESS_TOKEN are required.")
            self._facebook = FacebookTool(page_id=page_id, access_token=access_token)
        return self._facebook

    def load_json(
        self,
        idea_id: int,
        filename: str,
        model_class: Type[T],
    ) -> T:
        """
        Loads and validates a JSON file from the idea's root directory.
        """
        path = self.get_idea_path(idea_id) / filename
        if not path.exists():
            raise FileNotFoundError(f"Missing {filename} for project {idea_id}")
        return model_class.model_validate_json(path.read_text(encoding="utf-8"))

    def save_json(self, idea_id: int, filename: str, data: BaseModel):
        """
        Saves a Pydantic model as a JSON file in the idea's root directory.
        """
        path = self.get_idea_path(idea_id) / filename
        path.write_text(data.model_dump_json(indent=2), encoding="utf-8")

    def get_out_dir(self) -> Path:
        """
        Returns the absolute path to the base output directory.
        """
        self.out_base.mkdir(parents=True, exist_ok=True)
        return self.out_base

    def get_ideas_dir(self) -> Path:
        """
        Returns the absolute path to the global ideas folder.
        """
        path = self.get_out_dir() / self.IDEAS_DIR
        path.mkdir(parents=True, exist_ok=True)
        return path

    def get_idea_path(self, idea_id: int) -> Path:
        """
        Returns the absolute path to an idea's folder.
        """
        folder_name = f"idea_{idea_id:06d}"
        path = self.get_ideas_dir() / folder_name
        path.mkdir(parents=True, exist_ok=True)
        return path

    def get_idea_subdir(self, idea_id: int, subdir: str) -> Path:
        """
        Returns the absolute path to a subdirectory within an idea's folder
        """
        path = self.get_idea_path(idea_id) / subdir
        path.mkdir(parents=True, exist_ok=True)
        return path

    def get_idea_asset_path(self, idea_id: int, subdir: str, filename: str) -> Path:
        """
        Returns the absolute path to a file within an idea's subdirectory.
        """
        return self.get_idea_subdir(idea_id, subdir) / filename

    def get_named_video_path(self, idea_id: int, title: str) -> Path:
        """
        Derives the path for the final named video based on the idea title.
        """
        title_slug = slugify(title)
        return self.get_idea_path(idea_id) / f"{title_slug}.mp4"

    def step1_generate_story(self, extra_avoid: str = ""):
        """
        Generate Concept & Script: Creates a cinematic idea and expands it into a storyboard.
        1. Generates concept and script using PromptManager.
        2. Registers the new idea in tracking CSV.
        3. Saves idea.json and script.json.
        4. Updates state to SCRIPT_GENERATED.
        """
        Messenger.info("\n--- Generating cinematic concept and script ---")

        # Merge tracking CSV titles with extra avoid list
        titles = self.store.get_all_titles()

        # 1. Generates full story (Concept + Script)
        idea_data, script, category = self.prompt_manager.generate_full_story(
            self.text_gen, titles_to_avoid=titles, extra_avoid=extra_avoid
        )

        # 2. Registers the new idea in tracking CSV.
        idea_obj = self.store.add_new_idea(idea_data.title, category)

        # 3. Saves JSONs
        self.save_json(idea_obj.id, self.IDEA_JSON, idea_data)
        self.save_json(idea_obj.id, self.SCRIPT_JSON, script)

        # 4. Updates state
        idea_obj.state = State.SCRIPT_GENERATED
        self.store.save(idea_obj)
        Messenger.success(f"Step 1 ready: {State.SCRIPT_GENERATED} finalized.\n")

    def step2_generate_images(self):
        """
        Generate Images: Batch Image Generation (Gemini).
        Generates 3 frames per scene for Flipbook animation.
        """
        idea_obj = self.store.get_first_by_state(State.SCRIPT_GENERATED)
        if not idea_obj:
            Messenger.warning("Step 2 skipped: No idea in SCRIPT_GENERATED state.")
            return

        Messenger.info(f"Step 2 started: Generating Animated Frames for '{idea_obj.title}'")

        script = self.load_json(idea_obj.id, self.SCRIPT_JSON, VideoScript)

        # Determine if we are in Riddle mode or Video mode
        is_riddle = idea_obj.title.lower().startswith("acertijo") or "interaction" in str(type(idea_obj)).lower()
        
        # 5 Frames per scene for high-quality "Flipbook" animation (Videos only)
        # 1 Frame per scene for Riddles/Interaction Images
        frames_per_scene = 1 if is_riddle else 5
        
        tasks: List[ImageTask] = []
        for scene in script.scenes:
            # Revertido a 1 imagen pura y estática por escena
            action_prompt = scene.image_prompt
            out_name = f"scene_{scene.scene_number:02d}.png"
            out_path = self.get_idea_asset_path(idea_obj.id, self.IMAGES_DIR, out_name)
            tasks.append(
                ImageTask(
                    prompt=action_prompt,
                    output_path=out_path
                )
            )

        # Ensure directory exists
        if tasks:
            tasks[0].output_path.parent.mkdir(parents=True, exist_ok=True)

        # Generate all frames
        self.image_gen.generate_images(tasks)

        # Update State
        idea_obj.state = State.IMAGES_GENERATED
        self.store.save(idea_obj)
        Messenger.success(f"Step 2 ready: {State.IMAGES_GENERATED} finalized.\n")

    @retry(max_attempts=3)
    def step3_generate_audios(self):
        """
        Generate Audio: Batched AI-Guided Batching (Whisper + Gemini).
        Processes scenes in groups of 10 for maximum stability and alignment precision.
        """
        idea_obj = self.store.get_first_by_state(State.IMAGES_GENERATED)
        if not idea_obj:
            Messenger.error("No images ready for audio generation.")
            return

        Messenger.info("\n--- Generating batched audio for the script ---")
        script_data = self.load_json(idea_obj.id, self.SCRIPT_JSON, VideoScript)

        total_scenes = len(script_data.scenes)
        batch_size = 15

        for start_idx in range(0, total_scenes, batch_size):
            try:
                end_idx = min(start_idx + batch_size, total_scenes)
                chunk = script_data.scenes[start_idx:end_idx]
                batch_num = (start_idx // batch_size) + 1

                Messenger.info(f"Processing Batch {batch_num}: Scenes {start_idx + 1} to {end_idx}")

                # 1. Skip if all scenes in batch already exist
                missing_any = False
                for j in range(len(chunk)):
                    scene_num = start_idx + j + 1
                    out_path = self.get_idea_asset_path(
                        idea_obj.id, self.AUDIOS_DIR, self.SCENE_AUDIO_PATTERN.format(scene_num)
                    )
                    if not out_path.exists():
                        missing_any = True
                        break

                if not missing_any:
                    Messenger.info(f"Skipping Batch {batch_num}: All audio files exist.")
                    continue

                # 2. Synthesize chunk audio
                chunk_filename = self.BATCH_AUDIO_PATTERN.format(batch_num)
                chunk_audio_path = self.get_idea_asset_path(
                    idea_obj.id, self.AUDIOS_DIR, chunk_filename
                )

                Messenger.info(f"Synthesizing audio for Batch {batch_num}...")
                chunk_text = "\n\n".join([s.narration for s in chunk])
                formatted_audio = self.prompt_manager.get_audio_prompt(chunk_text)
                self.audio_gen.text_to_speech(formatted_audio, chunk_audio_path)

                # 3. Transcribe chunk
                Messenger.info(f"Transcribing Batch {batch_num} for alignment...")
                segments = self.whisper.get_transcription_segments(chunk_audio_path)

                # 4. Align chunk
                Messenger.info(f"Aligning Batch {batch_num} via Gemini...")
                chunk_script_texts = [s.narration for s in chunk]
                prompt = self.prompt_manager.get_alignment_prompt(segments, chunk_script_texts)
                alignment = self.text_gen.generate_text(prompt, AudioAlignment)

                # 5. Validate alignment count
                if len(alignment.alignments) != len(chunk):
                    # Delete corrupted chunk to force retry
                    chunk_audio_path.unlink(missing_ok=True)
                    chunk_audio_path.with_name(chunk_audio_path.name + ".json").unlink(missing_ok=True)
                    error_msg = (
                        f"Alignment mismatch in Batch {batch_num}: "
                        f"Expected {len(chunk)}, got {len(alignment.alignments)}"
                    )
                    raise RuntimeError(error_msg)

                # 6. Split and Save
                Messenger.info(f"Splitting Batch {batch_num} into {len(chunk)} scene audios...")
                for al in alignment.alignments:
                    # al.scene_number is 1-indexed relative to the chunk (1 to 10)
                    absolute_scene_num = start_idx + al.scene_number
                    out_path = self.get_idea_asset_path(
                        idea_obj.id,
                        self.AUDIOS_DIR,
                        self.SCENE_AUDIO_PATTERN.format(absolute_scene_num)
                    )

                    duration = al.end_time - al.start_time
                    if duration < 0.5:
                        chunk_audio_path.unlink(missing_ok=True)
                        chunk_audio_path.with_name(
                            chunk_audio_path.name + ".json"
                        ).unlink(missing_ok=True)
                        raise RuntimeError(
                            f"Invalid duration (Scene {absolute_scene_num}): "
                            f"{duration:.3f}s. Forcing retry."
                        )

                    self.ffmpeg.split_audio(
                        audio_in=chunk_audio_path,
                        audio_out=out_path,
                        start_time=al.start_time,
                        duration=duration
                    )

                # 7. Cleanup chunk audio
                chunk_audio_path.unlink(missing_ok=True)
            except Exception as e:
                import traceback
                Messenger.error(f"Error in batch {batch_num}: {str(e)}")
                Messenger.error(traceback.format_exc())
                raise e

        # Final Update
        idea_obj.state = State.AUDIO_GENERATED
        self.store.save(idea_obj)
        Messenger.success(f"Step 3 ready: {State.AUDIO_GENERATED} finalized.\n")

    def step4_generate_videos(self):
        """
        Video Generation: Creates clips for each scene and merges them.
        """
        # 1. Retrieves state
        idea_obj = self.store.get_first_by_state(State.AUDIO_GENERATED)
        if not idea_obj:
            Messenger.error("No audio ready for video generation.")
            return

        Messenger.info("\n--- Generating videos for the script ---")

        # 2. Loads script.json
        script_data = self.load_json(idea_obj.id, self.SCRIPT_JSON, VideoScript)
        
        # 3. Create Master Audio (Source of Truth)
        # This prevents gaps and desync by making one continuous audio file first.
        audio_segments = []
        for i in range(len(script_data.scenes)):
            seg = self.get_idea_asset_path(idea_obj.id, self.AUDIOS_DIR, self.SCENE_AUDIO_PATTERN.format(i + 1))
            audio_segments.append(seg)
        
        master_audio = self.get_idea_asset_path(idea_obj.id, self.EDITIONS_DIR, self.FINAL_AUDIO)
        # Custom concat for audio to ensure zero gaps
        audio_inputs = "".join([f"-i {str(s)} " for s in audio_segments])
        filter_complex = "".join([f"[{i}:a]" for i in range(len(audio_segments))]) + f"concat=n={len(audio_segments)}:v=0:a=1[a]"
        cmd = f"ffmpeg -y {audio_inputs}-filter_complex \"{filter_complex}\" -map \"[a]\" {str(master_audio)}"
        import os
        os.system(cmd)

        # 4. Merges assets into scene clips (Visual only)
        scene_videos: List[Path] = []
        for i, scene in enumerate(script_data.scenes):
            source_path = self.get_idea_asset_path(idea_obj.id, self.IMAGES_DIR, f"scene_{i+1:02d}_frame_01.png")
            if not source_path.exists():
                source_path = self.get_idea_asset_path(idea_obj.id, self.IMAGES_DIR, f"scene_{i+1:02d}.png")

            audio_seg = audio_segments[i]
            video_path = self.get_idea_asset_path(idea_obj.id, self.VIDEOS_DIR, self.SCENE_VIDEO_PATTERN.format(i + 1))

            Messenger.info(f"Stitching Scene {i+1}...")
            # We still need the audio segment for duration in this step
            if "_frame_" in str(source_path):
                image_sequence_pattern = str(source_path).replace("_frame_01.png", "_frame_%02d.png")
                self.ffmpeg.create_animated_scene_video(image_sequence_pattern, audio_seg, video_path)
            else:
                self.ffmpeg.create_composite_scene_video(source_path, audio_seg, video_path)
            scene_videos.append(video_path)

        # 5. Final video concatenation + Master Audio re-sync
        raw_video = self.get_idea_asset_path(idea_obj.id, self.EDITIONS_DIR, self.RAW_VIDEO)
        temp_video = self.get_idea_asset_path(idea_obj.id, self.VIDEOS_DIR, "temp_concat.mp4")
        self.ffmpeg.concat_videos(scene_videos, temp_video)
        
        # Merge concatenated video with the Master Audio to fix any drift
        cmd_merge = [
            "ffmpeg", "-y", "-i", str(temp_video), "-i", str(master_audio),
            "-c:v", "copy", "-c:a", "aac", "-map", "0:v:0", "-map", "1:a:0", "-shortest",
            str(raw_video)
        ]
        import subprocess
        subprocess.run(cmd_merge, check=True)

        # 6. Updates state.
        idea_obj.state = State.VIDEO_GENERATED
        self.store.save(idea_obj)
        Messenger.success(f"Step 4 ready: {State.VIDEO_GENERATED} finalized.\n")

    def step5_generate_subtitles(self):
        """
        Generate Subtitles: Adds subtitles to the video.
        1. Retrieves the VIDEO_GENERATED idea.
        2. Prepares directories.
        3. Extracts audio.
        4. Generates srt.
        5. Adds subtitles to final video.
        6. Updates state.
        """
        # 1. Retrieves VIDEO_GENERATED idea.
        idea_obj = self.store.get_first_by_state(State.VIDEO_GENERATED)
        if not idea_obj:
            Messenger.error("No video ready for subtitle generation.")
            return

        Messenger.info("\n--- Generating subtitles for the video ---")

        # 2. Prepares directories.
        raw_video = self.get_idea_asset_path(
            idea_obj.id, self.EDITIONS_DIR, self.RAW_VIDEO
        )
        audio_wav = self.get_idea_asset_path(
            idea_obj.id, self.EDITIONS_DIR, self.FINAL_AUDIO
        )
        subs_srt = self.get_idea_asset_path(
            idea_obj.id, self.EDITIONS_DIR, self.FINAL_SUBS
        )
        subtitled_video = self.get_idea_asset_path(
            idea_obj.id, self.EDITIONS_DIR, self.SUBTITLED_VIDEO
        )

        # 3. Extract Audio
        Messenger.info("Extracting audio for transcription...")
        self.ffmpeg.extract_audio(raw_video, audio_wav)

        # 4. Generate srt
        Messenger.info("Transcribing audio via Whisper.cpp...")
        self.whisper.generate_srt(audio_wav, subs_srt)

        # 5. Add Subtitles
        Messenger.info("Adding subtitles to final video...")
        self.ffmpeg.add_subtitles_to_video(raw_video, subs_srt, subtitled_video)

        # 6. Updates state.
        idea_obj.state = State.VIDEO_SUBTITLED
        self.store.save(idea_obj)
        Messenger.success(f"Step 5 ready: {State.VIDEO_SUBTITLED} finalized.\n")

    def step5_pro_subtitles(self):
        """
        Step 5 (PRO): High-End Subtitles and Multi-layer Composition.
        """
        # 1. Retrieves state
        idea_obj = self.store.get_first_by_state(State.VIDEO_GENERATED)
        if not idea_obj:
            Messenger.error("No video ready for PRO subtitles.")
            return

        raw_video = self.get_idea_asset_path(idea_obj.id, self.EDITIONS_DIR, self.RAW_VIDEO)
        remotion_overlay = self.get_idea_asset_path(idea_obj.id, self.EDITIONS_DIR, self.REMOTION_VIDEO)
        pro_video = self.get_idea_asset_path(idea_obj.id, self.EDITIONS_DIR, self.PRO_SUBTITLED_VIDEO)
        audio_wav = self.get_idea_asset_path(idea_obj.id, self.EDITIONS_DIR, self.FINAL_AUDIO)
        
        # 2. Transcription (Master Audio already exists from Step 4)
        Messenger.info(f"Transcribing {self.FINAL_AUDIO} with OpenAI Whisper...")
        words = self.whisper.get_word_tokens(audio_wav)
        word_data = [{"text": w.text, "start": w.start, "end": w.end} for w in words]

        # 3. Render Remotion
        remotion_root = Path(self.REMOTION_DIR)
        remotion_frames_dir = remotion_overlay.parent
        remotion_frames_dir.mkdir(parents=True, exist_ok=True)
        
        self.remotion.render_subtitles(
            remotion_path=remotion_root,
            output_path=remotion_overlay,
            data=word_data
        )

        # 4. Multi-layer Composition with filter_complex
        import subprocess
        remotion_pattern = remotion_overlay / "%04d.png"
        duration = self.ffmpeg.get_video_duration(raw_video)
        
        fc = (
            f"[0:v]noise=alls=5:allf=t+u[v_grain];"
            f"[v_grain]drawbox=y=ih-10:w=iw:h=10:color=black@0.5:t=fill[v_bar_bg];"
            f"[v_bar_bg]drawbox=y=ih-10:w=iw*t/{duration}:h=10:color=#FFFF00@0.8:t=fill[v_composed];"
            f"[v_composed][1:v]overlay=shortest=1[out]"
        )
        
        cmd = [
            "ffmpeg", "-y",
            "-i", str(raw_video),
            "-framerate", "25",
            "-i", str(remotion_pattern),
            "-filter_complex", fc,
            "-map", "[out]", "-map", "0:a",
            "-c:v", "libx264", "-c:a", "copy", "-pix_fmt", "yuv420p",
            str(pro_video)
        ]
        subprocess.run(cmd, check=True)

        # 5. Updates state
        idea_obj.state = State.VIDEO_PRO_SUBTITLED
        self.store.save(idea_obj)
        Messenger.success(f"Step 5 (PRO) ready: {State.VIDEO_PRO_SUBTITLED} finalized.\n")

    def step6_add_background_music(self):
        """
        Background Music: Adds a random background track to the subtitled video.
        """
        # 1. Retrieves subtitled video (PRO takes priority)
        idea_obj = self.store.get_first_by_state(State.VIDEO_PRO_SUBTITLED)
        is_pro = True
        if not idea_obj:
            idea_obj = self.store.get_first_by_state(State.VIDEO_SUBTITLED)
            is_pro = False
            
        if not idea_obj:
            Messenger.error("No subtitled video (Standard or PRO) found to add music.")
            return

        Messenger.info(f"\n--- Adding background music to {'PRO' if is_pro else 'Standard'} video ---")

        # 2. Prepares directories.
        subtitled_video = self.get_idea_asset_path(
            idea_obj.id, self.EDITIONS_DIR, 
            self.PRO_SUBTITLED_VIDEO if is_pro else self.SUBTITLED_VIDEO
        )
        final_with_music = self.get_idea_asset_path(
            idea_obj.id, self.EDITIONS_DIR, self.FINAL_VIDEO
        )

        # 3. Picks a random audio file
        selected_music = self.audio_tool.get_random_audio()
        if not selected_music:
            return

        # 4. Mixes it with low volume and looping.
        self.ffmpeg.add_background_music(
            subtitled_video,
            selected_music,
            final_with_music,
            bg_volume=0.18  # Subtle atmosphere
        )

        # 5. Updates state.
        idea_obj.state = State.VIDEO_MUSIC_GENERATED
        self.store.save(idea_obj)
        Messenger.success(f"Step 6 ready: {State.VIDEO_MUSIC_GENERATED} finalized.\n")

    def step7_rename_final_video(self):
        """
        Rename Final Video: Renames the final video to match the script title.
        1. Retrieves the VIDEO_MUSIC_GENERATED idea.
        2. Prepares directories.
        3. Renames the final video.
        4. Updates state.
        """
        # 1. Retrieves VIDEO_MUSIC_GENERATED idea.
        idea_obj = self.store.get_first_by_state(State.VIDEO_MUSIC_GENERATED)
        if not idea_obj:
            Messenger.error("No video with music found to rename.")
            return

        Messenger.info("\n--- Final Renaming: Naming video after script title ---")

        # 2. Prepares directories.
        final_video = self.get_idea_asset_path(
            idea_obj.id, self.EDITIONS_DIR, self.FINAL_VIDEO
        )
        if not final_video.exists():
            Messenger.error(f"Final video with music not found: {final_video}")
            return

        # 3. Renames the final video.
        video_title = idea_obj.title if idea_obj.title else f"video_{idea_obj.id}"
        named_final = self.get_named_video_path(idea_obj.id, video_title)
        final_video.rename(named_final)

        # 4. Updates state.
        idea_obj.state = State.COMPLETED
        self.store.save(idea_obj)
        Messenger.success(f"Step 7 ready: {State.COMPLETED} finalized.\n")

    def generate_facebook_description(self, title: str) -> str:
        """
        Generates a short, cynical, and highly viral description for Facebook/Instagram Reels.
        """
        prompt = f"""
        Eres el narrador de una serie llamada "EnigmaIQ". Eres autoritario, pedagógico y directo.
        Escribe la descripción para el siguiente video: "{title}"
        
        Requisitos OBLIGATORIOS:
        1. SE EXTREMADAMENTE CORTO. Máximo 2-3 líneas de texto. La gente no lee, ve el video.
        2. Tono: Maquiavélico y directo.
        3. Cierra con la frase de poder: "Síguenos en EnigmaIQ para más inteligencia financiera."
        4. Agrega exactamente 8 HASHTAGS VIRALES (ej: #FormasCochinas #InteligenciaFinanciera #Dinero #Negocios #Emprendimiento #MentalidadMilonaria #SecretosFinancieros #EnigmaIQ).
        
        Responde solo con el texto de la descripción, sin rodeos.
        """
        try:
            return self.text_gen.generate(prompt).strip()
        except Exception as e:
            Messenger.warning(f"AI Description generation failed: {e}. Using fallback.")
            return f"🔥 {title}\n\nSíguenos en EnigmaIQ para más inteligencia financiera.\n\n#FormasCochinas #InteligenciaFinanciera #Dinero #Negocios #Emprendimiento #MentalidadMilonaria #SecretosFinancieros #EnigmaIQ"

    def step8_upload_to_facebook(self):
        """
        Upload to Facebook: Uploads all COMPLETED videos to the configured Facebook Page.
        1. Retrieves all COMPLETED ideas.
        2. For each idea:
            a. Generates an AI-optimized description.
            b. Finds the final named video.
            c. Uploads via FacebookTool.
            d. Updates state to UPLOADED.
        """
        # 1. Retrieves COMPLETED ideas.
        # We use a loop to process all completed ones as requested by the user
        while True:
            idea_obj = self.store.get_first_by_state(State.COMPLETED)
            if not idea_obj:
                break

            Messenger.info(f"\n--- Uploading Idea {idea_obj.id}: {idea_obj.title} ---")

            # 2. Finds the final named video.
            video_title = idea_obj.title if idea_obj.title else f"video_{idea_obj.id}"
            video_path = self.get_named_video_path(idea_obj.id, video_title)

            if not video_path.exists():
                Messenger.error(f"Final video not found: {video_path}")
                # We skip this one to avoid infinite loop or mark it as error?
                # For now, let's just mark it as something else or break
                break

            # 3. Generates optimized description
            Messenger.info("   Generating AI-optimized description...")
            description = self.generate_facebook_description(video_title)

            # 4. Uploads via FacebookTool.
            try:
                self.facebook.upload_video(
                    file_path=video_path,
                    description=description,
                    title=video_title
                )
                
                # 5. Updates state to UPLOADED.
                idea_obj.state = State.UPLOADED
                self.store.save(idea_obj)
                Messenger.success(f"   Idea {idea_obj.id} uploaded and marked as {State.UPLOADED}.\n")
            except Exception as e:
                Messenger.error(f"   Failed to upload Idea {idea_obj.id}: {str(e)}")
                break
