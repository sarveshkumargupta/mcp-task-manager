from fastmcp import FastMCP
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware
from starlette.requests import Request
from starlette.responses import PlainTextResponse

from src.models import Task, add_task_to_file, list_tasks_from_file
    

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


# Configure CORS middleware for MCP Inspector (browser-based client)
middleware = [
    Middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Note: Use specific origins in production
        allow_methods=["GET", "POST", "DELETE", "OPTIONS"],
        allow_headers=[
            "mcp-protocol-version",
            "mcp-session-id",
            "Authorization",
            "Content-Type",
        ],
        expose_headers=["mcp-session-id"],
    )
]

# Create ASGI application
app = mcp.http_app(middleware=middleware)


if __name__ == "__main__":
    # Run with uvicorn ASGI server
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=9000)
