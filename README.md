# mcp-task-manager

A Model Context Protocol (MCP) server for task management. Built with FastMCP and async/await support for non-blocking file operations.

## Features

- ✨ **MCP Server** — Model Context Protocol implementation for task management
- ⚡ **Async Operations** — Non-blocking file I/O using `aiofiles`
- 🐳 **Docker Ready** — Includes Dockerfile and docker-compose configuration
- 📝 **Task Management** — Add, list, and manage tasks with structured schemas
- 🔍 **Health Check** — Built-in health check endpoint

## Prerequisites

- Python 3.11+
- [uv](https://docs.astral.sh/uv/) (package manager)
- Docker & Docker Compose (optional, for containerized deployment)

## Project Structure

```
mcp-task-manager/
├── src/
│   ├── server.py        # MCP server with HTTP transport
│   └── models.py        # Task model and file operations
├── data/
│   └── tasks.json       # Task storage (auto-created)
├── Dockerfile           # Docker configuration
├── docker-compose.yml   # Docker Compose setup
├── pyproject.toml       # Project dependencies
├── .python-version      # Python version specification
└── README.md
```

## Installation

### Local Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd mcp-task-manager
   ```

2. **Install dependencies**
   ```bash
   uv sync
   ```

3. **Run the server**
   ```bash
   python src/server.py
   ```

The server will start on `http://localhost:9000`

### Docker Setup

1. **Build and run with Docker Compose**
   ```bash
   docker-compose up --build
   ```

   Or build manually:
   ```bash
   docker build -t mcp-task-manager .
   docker run -p 9000:9000 -v $(pwd)/data:/app/data mcp-task-manager
   ```

## API Endpoints

### Health Check
- **GET** `/health` — Returns `OK` if the server is running

### MCP Tools

#### `add_task`
Add a new task to the manager.

**Parameters:**
- `title` (string): Task title
- `description` (string): Task description
- `task_type` (string): Either `"interview"` or `"study"`

**Returns:** Task ID

**Example:**
```python
add_task(
    title="Learn queue data structure",
    description="Use linkedlist to build queue",
    task_type="study"
)
```

#### `list_tasks`
Retrieve all tasks.

**Returns:** List of Task objects with their details

### MCP Resources

#### `data://tasks.json`
Provides the JSON schema for the Task model.

## Task Model

```python
Task(
    id: UUID                          # Auto-generated UUID
    title: str                        # Task title
    description: str                  # Task description
    task_type: Literal["interview", "study"]  # Task category
    completed: bool = False           # Completion status
)
```

## Configuration

### Environment Variables

- `PYTHONUNBUFFERED=1` — Ensures unbuffered output (set in Docker by default)

### Python Version

Specify Python version in `.python-version`:
```
3.11
```

## Development

### Code Quality

Run linting with Ruff:
```bash
ruff check .
```

### Dependencies

All dependencies are defined in `pyproject.toml`:
- `fastmcp` — MCP server framework
- `starlette` — Web framework
- `pydantic` — Data validation
- `aiofiles` — Async file operations

## Data Persistence

Tasks are stored in `data/tasks.json` as newline-delimited JSON (NDJSON format):

```json
{"id": "uuid...", "title": "Task 1", "description": "...", "task_type": "study", "completed": false}
{"id": "uuid...", "title": "Task 2", "description": "...", "task_type": "interview", "completed": false}
```

When running with Docker, mount the `data` directory as a volume to persist tasks:
```bash
docker run -v $(pwd)/data:/app/data mcp-task-manager
```

## Implementation Details

### Async/Await Support

- All file operations use `aiofiles` to prevent blocking the event loop
- MCP tools are async functions (`async def`)
- No thread pools needed for I/O operations

### Error Handling

Exceptions during file operations are caught and re-raised with descriptive error messages.