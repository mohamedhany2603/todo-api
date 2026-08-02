\# Task API



A simple CRUD API for managing tasks, built with FastAPI as part of the FlyRank Backend Internship (Week 2 assignment).



\## What this is



A backend API that lets a client create, read, update, and delete tasks, stored in memory (no database yet).



\## How to run



```

pip install fastapi uvicorn

uvicorn main:app --reload

```



Then visit `http://127.0.0.1:8000/docs` for interactive API docs (Swagger UI).



\## Endpoints



| Method | Path              | Description                  |

|--------|-------------------|-------------------------------|

| GET    | `/`                | API info                     |

| GET    | `/health`          | Health check                 |

| GET    | `/tasks`           | List all tasks               |

| GET    | `/tasks/{id}`      | Get a single task             |

| POST   | `/tasks`           | Create a new task             |

| PUT    | `/tasks/{id}`      | Update a task                 |

| DELETE | `/tasks/{id}`      | Delete a task                 |



\## Example request



```

curl -i http://127.0.0.1:8000/tasks/1

```



```

HTTP/1.1 200 OK

content-type: application/json



{"id":1,"title":"Updated title","done":true}

```



\## Swagger UI



!\[Swagger screenshot](swagger.png)

