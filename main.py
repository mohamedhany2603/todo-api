from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

class TaskInput(BaseModel):
    title: str
    done: bool = False

app = FastAPI()

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