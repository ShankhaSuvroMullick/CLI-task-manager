# models.py
from dataclasses import dataclass, asdict, field
from typing import Optional

@dataclass
class Task:
    id: int
    title: str
    done: bool = False
    due: Optional[str] = None
    priority: str = "medium"

    def to_dict(self) -> dict:
        return asdict(self)

    @staticmethod
    def from_dict(data: dict) -> "Task":
        return Task(
            id=data["id"],
            title=data["title"],
            done=data.get("done", False),
            due=data.get("due", None),
            priority=data.get("priority", "medium")
        )