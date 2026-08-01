from fastapi import FastAPI, HTTPException
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