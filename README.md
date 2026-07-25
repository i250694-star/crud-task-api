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

## Stage 7 — AI vs me

I gave an AI the following prompt and compared its generated API against my own hand-built version.

**Prompt used:**

> Build a REST API for managing a to-do list using Python and FastAPI. It needs these endpoints:
>
> - `GET /` — returns basic API info: name, version, and a list of available endpoints
> - `GET /health` — returns a simple status check, e.g. `{"status": "ok"}`
> - `GET /tasks` — returns the full list of tasks
> - `GET /tasks/{id}` — returns a single task matching that id; if no task has that id, return status 404 with a JSON error message
> - `POST /tasks` — creates a new task from a JSON body containing a `title`; validates that `title` is present and non-empty, returning status 400 if it's missing; on success, assigns the next available id, sets `done` to false, and returns status 201 with the created task
> - `PUT /tasks/{id}` — updates an existing task's `title` and/or `done` fields from the JSON body; returns the updated task, or 404 if the id doesn't exist
> - `DELETE /tasks/{id}` — removes the task with that id, returning status 204 with no body; returns 404 if the id doesn't exist
>
> Data should be stored in memory only (a Python list), with no database — data resets when the server restarts. It should also include Swagger UI (FastAPI provides this automatically at `/docs`) so I can test all endpoints interactively without curl.

**What the AI did better:** its validation used `.strip()` before checking if the title was empty, so a whitespace-only title (`"   "`) correctly gets rejected with 400. My own validation (`if not title`) doesn't catch this — I tested both side by side with the same request and my version incorrectly accepted a whitespace-only title as valid (201 Created), while the AI's correctly returned 400.

**What it got wrong or silently decided:** it started with an empty task list instead of pre-filled example tasks, and it used a running id counter instead of `max(existing ids) + 1` — meaning ids are never reused after a delete, unlike mine. Neither of these was specified in my prompt, so the AI just made a reasonable choice on its own.

**What my prompt forgot to specify:** I never mentioned seed/example data, or what should happen to task ids after a delete. Both silent decisions turned out reasonable, but it showed me my specification wasn't as complete as I thought it was.
