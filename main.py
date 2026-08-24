import sqlite3
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

class TaskInput(BaseModel):
    title: str
    done: bool = False

app = FastAPI()

conn = sqlite3.connect("tasks.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY,
        title TEXT,
        done INTEGER
    )
""")
conn.commit()

cursor.execute("SELECT COUNT(*) FROM tasks")
count = cursor.fetchone()[0]

if count == 0:
    cursor.execute("INSERT INTO tasks (title, done) VALUES (?, ?)", ("pray", 1))
    cursor.execute("INSERT INTO tasks (title, done) VALUES (?, ?)", ("study", 1))
    cursor.execute("INSERT INTO tasks (title, done) VALUES (?, ?)", ("play football", 0))
    conn.commit()

tasks = [
    {"id": 1, "title": "pray", "done": True},
    {"id": 2, "title": "study", "done": True},
    {"id": 3, "title": "play football", "done": False}
]

@app.get("/")
def read_root():
    return { "name": "Task API", "version": "1.0", "endpoints": ["/tasks"] }

@app.get("/health")
def check_health():
    return {"status": "ok"}

@app.get("/tasks")
def get_tasks():
    return tasks

@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    for i in tasks:
        if i["id"] == task_id:
            return i
    raise HTTPException(status_code=404, detail=f"Task {task_id} not found")

@app.post("/tasks", status_code=201)
def create_task(task: TaskInput):
    if not task.title or not task.title.strip():
        raise HTTPException(status_code=400, detail="Title is required")

    new_id = max(t["id"] for t in tasks) + 1
    new_task = {"id": new_id, "title": task.title, "done": False}
    tasks.append(new_task)
    return new_task

@app.put("/tasks/{task_id}")
def update_task(task_id: int, task: TaskInput):
    for i in tasks:
        if i["id"] == task_id:
            i["title"] = task.title
            i["done"] = task.done
            return i
    raise HTTPException(status_code=404, detail=f"Task {task_id} not found")

@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    for i in tasks:
        if i["id"] == task_id:
            tasks.remove(i)
            return {"message": f"Task {task_id} deleted"}
    raise HTTPException(status_code=404, detail=f"Task {task_id} not found")