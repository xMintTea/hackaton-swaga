import hashlib
from pathlib import Path


PATH = Path(__file__).parent.parent  / "config" / "accepted_origins.txt"


def get_hash(string: str) -> str:
    return hashlib.sha256(string.encode()).hexdigest()


def get_origins() -> list[str]:
    with open(PATH) as f:
        return f.read().splitlines()
    


if __name__ == "__main__":
    get_origins()