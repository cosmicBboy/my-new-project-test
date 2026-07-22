"""Data models for the TODO TUI app."""

from dataclasses import dataclass, field
from datetime import datetime, timedelta, date
from typing import Optional
from uuid import UUID, uuid4


@dataclass
class TodoItem:
    """Represents a single TODO item.
    
    Attributes:
        id: Unique identifier for the TODO item
        title: Description of the task
        completed: Whether the task is completed
        created_at: Timestamp when the task was created
        completed_at: Timestamp when the task was completed (None if not completed)
        postpone_until: Date until which the task is postponed (None if not postponed)
    """
    
    title: str
    id: UUID = field(default_factory=uuid4)
    completed: bool = False
    created_at: datetime = field(default_factory=datetime.now)
    completed_at: Optional[datetime] = None
    postpone_until: Optional[date] = None
    
    def toggle_completed(self) -> None:
        """Toggle the completion status of the TODO item."""
        self.completed = not self.completed
        if self.completed:
            self.completed_at = datetime.now()
        else:
            self.completed_at = None
    
    def postpone_until_tomorrow(self) -> None:
        """Postpone the TODO item until tomorrow.
        
        Sets the postpone_until date to tomorrow from today's date.
        """
        self.postpone_until = date.today() + timedelta(days=1)
    
    def is_postponed(self) -> bool:
        """Check if the TODO item is currently postponed.
        
        Returns:
            True if the item is postponed and the postpone date is in the future,
            False otherwise.
        """
        if self.postpone_until is None:
            return False
        return self.postpone_until > date.today()
    
    def clear_postpone(self) -> None:
        """Clear the postpone date."""
        self.postpone_until = None
    
    def to_dict(self) -> dict:
        """Convert the TODO item to a dictionary for serialization.
        
        Returns:
            Dictionary representation of the TODO item
        """
        return {
            "id": str(self.id),
            "title": self.title,
            "completed": self.completed,
            "created_at": self.created_at.isoformat(),
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
            "postpone_until": self.postpone_until.isoformat() if self.postpone_until else None,
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "TodoItem":
        """Create a TODO item from a dictionary.
        
        Args:
            data: Dictionary containing TODO item data
            
        Returns:
            TodoItem instance
        """
        return cls(
            id=UUID(data["id"]),
            title=data["title"],
            completed=data["completed"],
            created_at=datetime.fromisoformat(data["created_at"]),
            completed_at=(
                datetime.fromisoformat(data["completed_at"])
                if data.get("completed_at")
                else None
            ),
            postpone_until=(
                date.fromisoformat(data["postpone_until"])
                if data.get("postpone_until")
                else None
            ),
        )
    
    def __str__(self) -> str:
        """String representation of the TODO item."""
        status = "✓" if self.completed else " "
        postponed = " [postponed]" if self.is_postponed() else ""
        return f"[{status}] {self.title}{postponed}"
