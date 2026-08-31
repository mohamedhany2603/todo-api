import os
import psycopg
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Response
from pydantic import BaseModel

load_dotenv()

class TaskInput(BaseModel):
    title: str
    done: bool = False

app = FastAPI()

DATABASE_URL = os.getenv("DATABASE_URL")
conn = psycopg.connect(DATABASE_URL)
cursor = conn.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS tasks (
        id SERIAL PRIMARY KEY,
        title TEXT,
        done BOOLEAN
    )
""")
conn.commit()

cursor.execute("SELECT COUNT(*) FROM tasks")
count = cursor.fetchone()[0]

if count == 0:
    cursor.execute("INSERT INTO tasks (title, done) VALUES (%s, %s)", ("pray", True))
    cursor.execute("INSERT INTO tasks (title, done) VALUES (%s, %s)", ("study", True))
    cursor.execute("INSERT INTO tasks (title, done) VALUES (%s, %s)", ("play football", False))
    conn.commit()

tasks = [
    {"id": 1, "title": "pray", "done": 1},
    {"id": 2, "title": "study", "done": 1},
    {"id": 3, "title": "play football", "done": 0}
]

@app.get("/")
def read_root():
    return { "name": "Task API", "version": "1.0", "endpoints": ["/tasks"] }

@app.get("/health")
def check_health():
    return {"status": "ok"}

@app.get("/tasks")
def get_tasks():
    cursor.execute("SELECT * FROM tasks")
    rows = cursor.fetchall()
    result = []
    for r in rows:
        result.append({"id": r[0], "title": r[1], "done": bool(r[2])})
    return result

@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    cursor.execute("SELECT * FROM tasks WHERE id = %s", (task_id,))
    row = cursor.fetchone()
    if row:
        return {"id": row[0], "title": row[1], "done": bool(row[2])}
    raise HTTPException(status_code=404, detail=f"Task {task_id} not found")

@app.post("/tasks", status_code=201)
def create_task(task: TaskInput):
    if not task.title or not task.title.strip():
        raise HTTPException(status_code=400, detail="Title is required")

    cursor.execute("INSERT INTO tasks (title, done) VALUES (%s, %s) RETURNING id", (task.title, False))
    new_id = cursor.fetchone()[0]
    conn.commit()

    
    return {"id": new_id, "title": task.title, "done": False}

@app.put("/tasks/{task_id}")
def update_task(task_id: int, task: TaskInput):
    cursor.execute("SELECT * FROM tasks WHERE id = %s", (task_id,))
    row = cursor.fetchone()
    if not row:
        raise HTTPException(status_code=404, detail=f"Task {task_id} not found")

    if not task.title or not task.title.strip():
        raise HTTPException(status_code=400, detail="Title is required")

    cursor.execute("UPDATE tasks SET title = %s, done = %s WHERE id = %s", (task.title, task.done, task_id))
    conn.commit()

    return {"id": task_id, "title": task.title, "done": task.done}
@app.delete("/tasks/{task_id}", status_code=204)
def delete_task(task_id: int):
    cursor.execute("SELECT * FROM tasks WHERE id = %s", (task_id,))
    row = cursor.fetchone()
    if not row:
        raise HTTPException(status_code=404, detail=f"Task {task_id} not found")
    cursor.execute("DELETE FROM tasks WHERE id = %s", (task_id,))
    conn.commit()
    return Response(status_code=204)
    
