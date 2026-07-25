# Task API

A small CRUD (Create, Read, Update, Delete) API for managing a to-do list, built with FastAPI. Tasks are stored in memory (no database yet) and the API is fully documented and testable through Swagger UI.

## How to run it

1. Install dependencies:
   ```
   pip install fastapi uvicorn
   ```

2. Start the server:
   ```
   python -m uvicorn main:app --reload
   ```

3. The API is now running at `http://127.0.0.1:8000`

4. Interactive docs (Swagger UI) are available at `http://127.0.0.1:8000/docs`

## Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/` | API info (name, version, endpoints) |
| GET | `/health` | Health check — confirms the server is alive |
| GET | `/tasks` | List all tasks |
| GET | `/tasks/{task_id}` | Get a single task by id |
| POST | `/tasks` | Create a new task |
| PUT | `/tasks/{task_id}` | Update an existing task's title and/or done status |
| DELETE | `/tasks/{task_id}` | Delete a task |

## Status codes

| Code | Meaning | When it happens |
|------|---------|------------------|
| 200 | OK | Successful read or update |
| 201 | Created | Task successfully created |
| 204 | No Content | Task successfully deleted |
| 400 | Bad Request | Missing or empty `title` on create/update |
| 404 | Not Found | No task exists with the given id |

## Example request

```
curl -i -X POST http://127.0.0.1:8000/tasks -H "Content-Type: application/json" -d '{"title": "Test task"}'
```

Response:
```
HTTP/1.1 201 Created
content-type: application/json

{"id":4,"title":"Test task","done":false}
```

## Swagger UI

Every endpoint is listed and testable via "Try it out" at `/docs`.

![Swagger UI screenshot](swagger-screenshot.png)

## Note on data persistence

Tasks are stored only in memory — restarting the server resets the list back to its original 3 example tasks. This is intentional for this stage of the project; a real database (coming in a later stage) will fix this.
