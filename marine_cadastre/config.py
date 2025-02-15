from pathlib import Path
from dataclasses import dataclass


@dataclass()
class Config:
    data_dir: Path = Path("./data")
