import aiofiles
from pathlib import Path
from typing import Literal
from uuid import UUID, uuid4
from pydantic import BaseModel, Field


# Ensure data directory exists and use absolute path
DATA_DIR = Path(__file__).parent.parent / "data"
DATA_DIR.mkdir(exist_ok=True)
TASKS_FILE = DATA_DIR / "tasks.json"


class Task(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    title: str
    description: str
    task_type: Literal["interview", "study"]
    completed: bool = False


async def add_task_to_file(task: Task):
    try:
        async with aiofiles.open(str(TASKS_FILE), "a") as f:
            await f.write(task.model_dump_json() + "\n")
    except Exception as e:
        raise Exception(f"Failed to write task to file: {e}")


async def list_tasks_from_file() -> list[Task]:
    try:
        async with aiofiles.open(str(TASKS_FILE), "r") as f:
            content = await f.read()
            tasks = [Task.model_validate_json(line) for line in content.strip().split("\n") if line]
        return tasks
    except Exception as e:
        raise Exception(f"Failed to read tasks from file: {e}")
    