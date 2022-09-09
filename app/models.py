from dataclasses import dataclass

@dataclass
class User:
    """
    Data class to keep information about User model
    """
    tg_id: int
    first_name: str = None
    last_name: str = None
    username: str = None
    max_score: int = 0
