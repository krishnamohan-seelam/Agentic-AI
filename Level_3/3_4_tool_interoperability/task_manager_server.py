"""
Task Manager MCP Server - Practice Exercise

Build an MCP server that provides tools for managing a task/todo list.
This exercise reinforces the FastMCP patterns from the guided practice.

Your tasks:
1. Initialize the FastMCP server
2. Implement 5 MCP tools

Tools to implement:
- add_task: Add a new task with title, priority, and optional due date
- list_tasks: List tasks with optional status filter
- complete_task: Mark a task as completed
- delete_task: Remove a task
- get_task: Get details of a specific task

Run this server:
    python task_manager_server.py

Test with the provided notebook: 3_5_mcp_server_try_it.ipynb

Estimated time: 15-20 minutes
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Optional
from uuid import uuid4
from fastmcp import FastMCP

mcp = FastMCP(
    name="TaskManager",
    instructions="Provide tools to add, list, complete, delete, and fetch tasks stored persistently so users can manage their todo list.",
)


# =============================================================================
# Storage Configuration (provided)
# =============================================================================

STORAGE_DIR = Path(__file__).parent / "data"
STORAGE_FILE = STORAGE_DIR / "tasks.json"


def _ensure_storage():
    """Ensure the storage directory and file exist."""
    STORAGE_DIR.mkdir(exist_ok=True)
    if not STORAGE_FILE.exists():
        STORAGE_FILE.write_text(json.dumps({"tasks": {}}, indent=2))


def _load_tasks() -> dict:
    """Load tasks from storage."""
    _ensure_storage()
    return json.loads(STORAGE_FILE.read_text())


def _save_tasks(data: dict):
    """Save tasks to storage."""
    _ensure_storage()
    STORAGE_FILE.write_text(json.dumps(data, indent=2))


@mcp.tool()
def add_task(
    title: str, priority: str = "medium", due_date: Optional[str] = None
) -> dict:
    """
    Add a new task to the task manager.

    Args:
        title: The title/description of the task
        priority: Priority level - must be "high", "medium", or "low" (default: "medium")
        due_date: Optional due date in YYYY-MM-DD format (e.g., "2025-12-31")

    Returns:
        A dict with:
        - "status": "success" or "error"
        - "message": Description of what happened
        - "task": The created task object (if successful) containing:
            - id: 8-character unique ID
            - title: The task title
            - priority: The priority level
            - due_date: The due date or None
            - completed: False (new tasks start incomplete)
            - created_at: ISO timestamp
    """
    if priority not in ["high", "medium", "low"]:
        return {
            "status": "error",
            "message": "Priority must be 'high', 'medium', or 'low'",
        }

    tasks = _load_tasks()
    task_id = str(uuid4())[:8]
    tasks["tasks"][task_id] = {
        "id": task_id,
        "title": title,
        "priority": priority,
        "due_date": due_date,
        "completed": False,
        "created_at": datetime.now().isoformat(),
    }
    _save_tasks(tasks)
    return {
        "status": "success",
        "message": "Task added successfully",
        "task": tasks["tasks"][task_id],
    }


@mcp.tool()
def list_tasks(status_filter: Optional[str] = None) -> dict:
    """
    List all tasks, optionally filtered by completion status.

    Args:
        status_filter: Optional filter - "completed", "pending", or None for all tasks

    Returns:
        A dict with:
        - "status": "success"
        - "total_count": Total number of tasks in storage
        - "returned_count": Number of tasks after filtering
        - "filter_applied": The filter that was used (or None)
        - "tasks": List of task objects sorted by priority (high first)
    """
    tasks = _load_tasks()
    task_list = list(tasks["tasks"].values())
    if status_filter == "completed":
        task_list = [t for t in task_list if t["completed"]]
    elif status_filter == "pending":
        task_list = [t for t in task_list if not t["completed"]]

    task_list.sort(key=lambda t: ["high", "medium", "low"].index(t["priority"]))
    return {
        "status": "success",
        "total_count": len(tasks["tasks"]),
        "returned_count": len(task_list),
        "filter_applied": status_filter,
        "tasks": task_list,
    }


@mcp.tool()
def complete_task(task_id: str) -> dict:
    """
    Mark a task as completed.

    Args:
        task_id: The unique identifier of the task to complete

    Returns:
        A dict with:
        - "status": "success" or "error"
        - "message": Description of what happened
        - "task": The updated task object (if successful)
    """
    tasks = _load_tasks()
    if task_id not in tasks["tasks"]:
        return {"status": "error", "message": f"Task {task_id} not found"}
    tasks["tasks"][task_id]["completed"] = True
    _save_tasks(tasks)
    return {
        "status": "success",
        "message": f"Task {task_id} marked as completed",
        "task": tasks["tasks"][task_id],
    }


@mcp.tool()
def delete_task(task_id: str) -> dict:
    """
    Delete a task from the task manager.

    Args:
        task_id: The unique identifier of the task to delete

    Returns:
        A dict with:
        - "status": "success" or "error"
        - "message": Description of what happened (include task title if deleted)
    """
    tasks = _load_tasks()
    if task_id not in tasks["tasks"]:
        return {"status": "error", "message": f"Task {task_id} not found"}
    task_title = tasks["tasks"][task_id]["title"]
    del tasks["tasks"][task_id]
    _save_tasks(tasks)
    return {
        "status": "success",
        "message": f"Task {task_title} deleted successfully",
        "task_id": task_id,
    }


@mcp.tool()
def get_task(task_id: str) -> dict:
    """
    Get details of a specific task by ID.

    Args:
        task_id: The unique identifier of the task

    Returns:
        A dict with:
        - "status": "success" or "error"
        - "task": The task object (if found)
        - "message": Error message (if not found)
    """
    tasks = _load_tasks()
    if task_id not in tasks["tasks"]:
        return {"status": "error", "message": f"Task {task_id} not found"}
    return {"status": "success", "task": tasks["tasks"][task_id]}


# =============================================================================
# Server Entry Point
# =============================================================================

if __name__ == "__main__":
    print("Starting Task Manager MCP Server...")
    print(f"Storage location: {STORAGE_FILE}")
    mcp.run(transport="stdio")
