"""Tests for the data models."""

import pytest
from datetime import datetime
from uuid import UUID

from todo_tui.models import TodoItem


def test_todo_item_creation():
    """Test creating a basic TODO item."""
    todo = TodoItem(title="Test task")
    
    assert todo.title == "Test task"
    assert isinstance(todo.id, UUID)
    assert todo.completed is False
    assert isinstance(todo.created_at, datetime)
    assert todo.completed_at is None


def test_todo_item_toggle_completed():
    """Test toggling completion status."""
    todo = TodoItem(title="Test task")
    
    # Initially not completed
    assert todo.completed is False
    assert todo.completed_at is None
    
    # Toggle to completed
    todo.toggle_completed()
    assert todo.completed is True
    assert isinstance(todo.completed_at, datetime)
    
    # Toggle back to not completed
    todo.toggle_completed()
    assert todo.completed is False
    assert todo.completed_at is None


def test_todo_item_to_dict():
    """Test serialization to dictionary."""
    todo = TodoItem(title="Test task")
    data = todo.to_dict()
    
    assert data["title"] == "Test task"
    assert data["completed"] is False
    assert "id" in data
    assert "created_at" in data
    assert data["completed_at"] is None


def test_todo_item_from_dict():
    """Test deserialization from dictionary."""
    original = TodoItem(title="Test task")
    data = original.to_dict()
    
    restored = TodoItem.from_dict(data)
    
    assert restored.id == original.id
    assert restored.title == original.title
    assert restored.completed == original.completed
    assert restored.created_at == original.created_at
    assert restored.completed_at == original.completed_at


def test_todo_item_from_dict_with_completion():
    """Test deserialization of a completed TODO."""
    original = TodoItem(title="Test task")
    original.toggle_completed()
    data = original.to_dict()
    
    restored = TodoItem.from_dict(data)
    
    assert restored.completed is True
    assert isinstance(restored.completed_at, datetime)


def test_todo_item_str():
    """Test string representation."""
    todo = TodoItem(title="Test task")
    
    assert str(todo) == "[ ] Test task"
    
    todo.toggle_completed()
    assert str(todo) == "[✓] Test task"
