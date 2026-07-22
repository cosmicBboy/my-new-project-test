"""Tests for the data models."""

import pytest
from datetime import datetime, date, timedelta
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
    assert todo.postpone_until is None


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


def test_todo_item_postpone_until_tomorrow():
    """Test postponing a TODO until tomorrow."""
    todo = TodoItem(title="Test task")
    
    # Initially not postponed
    assert todo.postpone_until is None
    assert todo.is_postponed() is False
    
    # Postpone until tomorrow
    todo.postpone_until_tomorrow()
    assert todo.postpone_until == date.today() + timedelta(days=1)
    assert todo.is_postponed() is True


def test_todo_item_postpone_multiple_times():
    """Test postponing a TODO multiple times.
    
    Postponing always sets the date to tomorrow from today,
    not progressively advancing from the previous postpone date.
    """
    todo = TodoItem(title="Test task")
    
    # First postpone
    todo.postpone_until_tomorrow()
    first_postpone_date = todo.postpone_until
    assert first_postpone_date == date.today() + timedelta(days=1)
    
    # Second postpone (same day) - should still be tomorrow
    todo.postpone_until_tomorrow()
    assert todo.postpone_until == date.today() + timedelta(days=1)
    assert todo.postpone_until == first_postpone_date


def test_todo_item_clear_postpone():
    """Test clearing the postpone date."""
    todo = TodoItem(title="Test task")
    
    # Postpone the todo
    todo.postpone_until_tomorrow()
    assert todo.is_postponed() is True
    
    # Clear the postpone
    todo.clear_postpone()
    assert todo.postpone_until is None
    assert todo.is_postponed() is False


def test_todo_item_is_postponed_past_date():
    """Test that past postpone dates are not considered postponed."""
    todo = TodoItem(title="Test task")
    
    # Set postpone date to yesterday
    todo.postpone_until = date.today() - timedelta(days=1)
    assert todo.is_postponed() is False
    
    # Set postpone date to today - should be considered postponed
    todo.postpone_until = date.today()
    assert todo.is_postponed() is True
    
    # Set postpone date to tomorrow
    todo.postpone_until = date.today() + timedelta(days=1)
    assert todo.is_postponed() is True


def test_todo_item_to_dict():
    """Test serialization to dictionary."""
    todo = TodoItem(title="Test task")
    data = todo.to_dict()
    
    assert data["title"] == "Test task"
    assert data["completed"] is False
    assert "id" in data
    assert "created_at" in data
    assert data["completed_at"] is None
    assert data["postpone_until"] is None


def test_todo_item_to_dict_with_postpone():
    """Test serialization with postpone date."""
    todo = TodoItem(title="Test task")
    todo.postpone_until_tomorrow()
    data = todo.to_dict()
    
    assert data["postpone_until"] is not None
    assert data["postpone_until"] == (date.today() + timedelta(days=1)).isoformat()


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
    assert restored.postpone_until == original.postpone_until


def test_todo_item_from_dict_with_completion():
    """Test deserialization of a completed TODO."""
    original = TodoItem(title="Test task")
    original.toggle_completed()
    data = original.to_dict()
    
    restored = TodoItem.from_dict(data)
    
    assert restored.completed is True
    assert isinstance(restored.completed_at, datetime)


def test_todo_item_from_dict_with_postpone():
    """Test deserialization of a postponed TODO."""
    original = TodoItem(title="Test task")
    original.postpone_until_tomorrow()
    data = original.to_dict()
    
    restored = TodoItem.from_dict(data)
    
    assert restored.postpone_until is not None
    assert restored.postpone_until == original.postpone_until
    assert restored.is_postponed() is True


def test_todo_item_str():
    """Test string representation."""
    todo = TodoItem(title="Test task")
    
    assert str(todo) == "[ ] Test task"
    
    todo.toggle_completed()
    assert str(todo) == "[✓] Test task"


def test_todo_item_str_postponed():
    """Test string representation of postponed TODO."""
    todo = TodoItem(title="Test task")
    todo.postpone_until_tomorrow()
    
    assert "[ ] Test task [postponed]" == str(todo)
