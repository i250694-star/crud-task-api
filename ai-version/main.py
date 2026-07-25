"""
Simple in-memory To-Do List REST API built with FastAPI.

Run with:
    pip install fastapi uvicorn --break-system-packages
    uvicorn main:app --reload

Then open http://127.0.0.1:8000/docs for the interactive Swagger UI.
"""

from typing import List, Optional

from fastapi import FastAPI, HTTPException, status
from fastapi.responses import Response
from pydantic import BaseModel, Field

app = FastAPI(
    title="To-Do List API",
    version="1.0.0",
    description="A simple in-memory REST API for managing a to-do list.",
)


# ---------------------------------------------------------------------------
# Models
# ---------------------------------------------------------------------------

class Task(BaseModel):
    id: int
    title: str
    done: bool = False


class TaskCreate(BaseModel):
    title: Optional[str] = None


class TaskUpdate(BaseModel):
    title: Optional[str] = None
    done: Optional[bool] = None


# ---------------------------------------------------------------------------
# In-memory storage
# ---------------------------------------------------------------------------

tasks: List[Task] = []
_next_id = 1


def _get_next_id() -> int:
    global _next_id
    current = _next_id
    _next_id += 1
    return current


def _find_task(task_id: int) -> Optional[Task]:
    for task in tasks:
        if task.id == task_id:
            return task
    return None


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------

@app.get("/")
def read_root():
    """Basic API info and a list of available endpoints."""
    return {
        "name": "To-Do List API",
        "version": app.version,
        "endpoints": [
            {"method": "GET", "path": "/", "description": "API info"},
            {"method": "GET", "path": "/health", "description": "Health check"},
            {"method": "GET", "path": "/tasks", "description": "List all tasks"},
            {"method": "GET", "path": "/tasks/{id}", "description": "Get a single task"},
            {"method": "POST", "path": "/tasks", "description": "Create a new task"},
            {"method": "PUT", "path": "/tasks/{id}", "description": "Update a task"},
            {"method": "DELETE", "path": "/tasks/{id}", "description": "Delete a task"},
        ],
    }


@app.get("/health")
def health_check():
    """Simple health check."""
    return {"status": "ok"}


@app.get("/tasks", response_model=List[Task])
def get_tasks():
    """Return the full list of tasks."""
    return tasks


@app.get("/tasks/{task_id}", response_model=Task)
def get_task(task_id: int):
    """Return a single task by id, or 404 if it doesn't exist."""
    task = _find_task(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail=f"Task with id {task_id} not found")
    return task


@app.post("/tasks", response_model=Task, status_code=status.HTTP_201_CREATED)
def create_task(payload: TaskCreate):
    """Create a new task. Requires a non-empty 'title'."""
    if payload.title is None or not payload.title.strip():
        raise HTTPException(status_code=400, detail="Field 'title' is required and cannot be empty")

    task = Task(id=_get_next_id(), title=payload.title.strip(), done=False)
    tasks.append(task)
    return task


@app.put("/tasks/{task_id}", response_model=Task)
def update_task(task_id: int, payload: TaskUpdate):
    """Update an existing task's title and/or done status."""
    task = _find_task(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail=f"Task with id {task_id} not found")

    if payload.title is not None:
        if not payload.title.strip():
            raise HTTPException(status_code=400, detail="Field 'title' cannot be empty")
        task.title = payload.title.strip()

    if payload.done is not None:
        task.done = payload.done

    return task


@app.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: int):
    """Delete a task by id. Returns 204 on success, 404 if not found."""
    task = _find_task(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail=f"Task with id {task_id} not found")

    tasks.remove(task)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
