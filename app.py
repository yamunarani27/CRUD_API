from fastapi import FastAPI,HTTPException, status
from pydantic import BaseModel


app = FastAPI()

tasks=[
    {"id":1,"title":"Refresh and have a coffee","done":True},
    {"id":2,"title":"Walk for 30 mins","done":False},
    {"id":3,"title":"Login to swedish class","done":False}
    ]

class Item(BaseModel):
    title: str | None = None

@app.get("/")
async def root():
    return {"name": "Task API","version":"1.0","endpoints":["/tasks"]}

@app.get("/health")
async def health():
    return {"status":"ok"}

@app.get("/tasks")
async def get_tasks():
    return tasks

@app.get("/tasks/{id}")
async def get_task(id:int):
    for task in tasks:
        if task["id"] == id:
           return task
        
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail={"error": f"Task {id} not found"}
    )

@app.post("/tasks",status_code=status.HTTP_201_CREATED)
async def new_task(item:Item):

    if not item.title or not item.title.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,   
            detail={"error": f"Title is missing or empty"}
        )
    new_id = max([t["id"] for t in tasks], default=0) + 1
    
    # Create the new task object setting done to false
    created_task = {
        "id": new_id,
        "title": item.title.strip(),
        "done": False
    }
    
    # Add it to the list
    tasks.append(created_task)
    
    # Return the created task
    return created_task
