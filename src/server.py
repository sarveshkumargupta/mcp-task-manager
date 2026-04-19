from fastmcp import FastMCP
from starlette.requests import Request
from starlette.responses import PlainTextResponse

from models import Task, add_task_to_file, list_tasks_from_file
    

mcp = FastMCP("Sarvesh's task manager")


@mcp.custom_route("/health", methods=["GET"])
async def health_check(request: Request) -> PlainTextResponse:
    return PlainTextResponse("OK")


@mcp.resource("data://tasks.json")
def tasks_resource():
    """Provides schema for tasks.json file"""
    return Task.model_json_schema()


@mcp.tool
async def add_task(task: Task) -> str:
    """Add a new task"""
    await add_task_to_file(task)
    return f"Task added with ID: {task.id}"


@mcp.tool
async def list_tasks() -> list[Task]:
    """Get a list of all tasks"""
    return await list_tasks_from_file()


if __name__ == "__main__":
    # Run with HTTP transport
    mcp.run(transport="http", host="0.0.0.0", port=9000)
