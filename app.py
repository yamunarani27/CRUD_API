from fastapi import FastAPI,HTTPException, status

app = FastAPI()

tasks=[
    {"id":1,"title":"Refresh and have a coffee","done":True},
    {"id":2,"title":"Walk for 30 mins","done":False},
    {"id":3,"title":"Login to swedish class","done":False}
    ]

@app.get("/")
async def root():
    return {"name": "Task API","version":"1.0","endpoints":["/tasks"]}

@app.get("/health")
async def health():
    return {"status":"ok"}

@app.get("/tasks")
async def get_tasks():
    return tasks

@app.get("/task/{id}")
async def get_task(id:int):
    for task in tasks:
        if task["id"] == id:
           return task
        
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail={"error": f"Task {id} not found"}
    )
    