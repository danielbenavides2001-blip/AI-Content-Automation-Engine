import os
import time
from pathlib import Path
from typing import Any, Dict, List

import pandas as pd

from tools.common.base_model import BaseModelTool


class FileLock:
    """Cross-platform file-based lock using O_EXCL."""
    def __init__(self, lock_path: Path, timeout: float = 30.0):
        self.lock_path = lock_path
        self.timeout = timeout
        self.fd = None

    def __enter__(self):
        deadline = time.time() + self.timeout
        while True:
            try:
                self.fd = os.open(str(self.lock_path), os.O_CREAT | os.O_EXCL | os.O_RDWR)
                break
            except FileExistsError:
                if time.time() > deadline:
                    self.lock_path.unlink(missing_ok=True)
                    self.fd = os.open(str(self.lock_path), os.O_CREAT | os.O_EXCL | os.O_RDWR)
                    break
                time.sleep(0.05)
        return self

    def __exit__(self, *args):
        if self.fd is not None:
            os.close(self.fd)
            self.fd = None
        self.lock_path.unlink(missing_ok=True)


class CsvProcessor(BaseModelTool):
    """
    Generic tool for basic CSV operations using pandas.
    """
    path: Path
    required_columns: List[str]

    def __init__(self, **kwargs: Any):
        super().__init__(**kwargs)
        self._ensure_file_exists()

    def _lock_path(self) -> Path:
        return self.path.with_name(self.path.name + ".lock")

    def _ensure_file_exists(self) -> None:
        if not self.path.exists():
            self.path.parent.mkdir(parents=True, exist_ok=True)
            df = pd.DataFrame(columns=list(self.required_columns))
            df.to_csv(self.path, index=False)
        else:
            self.validate_structure()

    def validate_structure(self) -> None:
        if not self.required_columns:
            return
        df = pd.read_csv(self.path)
        for col in self.required_columns:
            if col not in df.columns:
                raise ValueError(f"Invalid CSV structure at {self.path}. Missing column: {col}")

    def read_all(self) -> pd.DataFrame:
        return pd.read_csv(self.path)

    def write_all(self, df: pd.DataFrame) -> None:
        df.to_csv(self.path, index=False)

    def get_row(self, index: int) -> Dict[str, Any]:
        with FileLock(self._lock_path()):
            df = self.read_all()
            return dict(df.iloc[index])

    def update_row(self, index: int, data: Dict[str, Any]) -> None:
        with FileLock(self._lock_path()):
            df = self.read_all()
            for key, value in data.items():
                if df[key].dtype == "float64" and isinstance(value, str):
                    df[key] = df[key].astype(object)
                df.at[index, key] = value
            self.write_all(df)

    def add_row(self, data: Dict[str, Any]) -> None:
        with FileLock(self._lock_path()):
            df = self.read_all()
            new_row = pd.DataFrame([data])
            df = pd.concat([df, new_row], ignore_index=True)
            self.write_all(df)
