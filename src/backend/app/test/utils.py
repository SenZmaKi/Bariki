from pathlib import Path

ROOT_DIR = Path(__file__).parent

def join_from_root(path: str) -> Path:
    return ROOT_DIR / path
