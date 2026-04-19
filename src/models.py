import aiofiles
import os
from typing import Literal
from uuid import UUID, uuid4
from pydantic import BaseModel, Field


# Determine storage mode from environment variable
STORAGE_MODE = os.getenv("STORAGE_MODE", "file").lower()  # "file" or "memory"


class Task(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    title: str
    description: str
    task_type: Literal["interview", "study"]
    completed: bool = False


# In-memory storage for platforms like horizon
_tasks_memory: list[Task] = []


async def add_task_to_file(task: Task):
    """Add task to storage (file or memory based on STORAGE_MODE)"""
    if STORAGE_MODE == "memory":
        _tasks_memory.append(task)
    else:
        # File-based storage (local/Docker)
        try:
            async with aiofiles.open("data/tasks.json", "a") as f:
                await f.write(task.model_dump_json() + "\n")
        except Exception as e:
            raise Exception(f"Failed to write task to file: {e}")


async def list_tasks_from_file() -> list[Task]:
    """List all tasks from storage (file or memory based on STORAGE_MODE)"""
    if STORAGE_MODE == "memory":
        return _tasks_memory
    else:
        # File-based storage (local/Docker)
        try:
            async with aiofiles.open("data/tasks.json", "r") as f:
                content = await f.read()
                tasks = [Task.model_validate_json(line) for line in content.strip().split("\n") if line]
            return tasks
        except Exception as e:
            raise Exception(f"Failed to read tasks from file: {e}")
        