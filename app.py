from fastapi import FastAPI,HTTPException, status,Response
from pydantic import BaseModel


app = FastAPI()

tasks=[
    {"id":1,"title":"Refresh and have a coffee","done":True},
    {"id":2,"title":"Walk for 30 mins","done":False},
    {"id":3,"title":"Login to swedish class","done":False}
    ]

class Item(BaseModel):
    title: str | None = None
    done: bool | None = None

@app.get("/")
async def root():
    return {"name": "Task API","version":"1.0","endpoints":["/tasks"]}

@app.get("/health")
async def health():
    """Checks a server is alive"""
    return {"status":"ok"}

@app.get("/tasks")
async def get_tasks():
    """Retrieves all the tasks and displays in a list"""
    return tasks

@app.get("/tasks/{id}")
async def get_task_by_id(id:int):
    """Retrieves only the task with a given id from the list"""
    for task in tasks:
        if task["id"] == id:
           return task
        
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail={"error": f"Task {id} not found"}
    )

@app.post("/tasks",status_code=status.HTTP_201_CREATED)
async def create_task(item:Item):
    """Creates a new task and add it to the list"""
    if not item.title or not item.title.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,   
            detail={"error": f"Title is missing or empty"}
        )
    new_id = max([t["id"] for t in tasks], default=0) + 1
    
    created_task = {
        "id": new_id,
        "title": item.title.strip(),
        "done": False
    }
    
    tasks.append(created_task)
    
    return created_task

@app.put("/tasks/{id}",response_model=Item)
async def update_task(id: int, item: Item):
    """select the task with a given id and update its content"""

    if item.title is None and item.done is None:
        raise HTTPException(
         status_code=status.HTTP_400_BAD_REQUEST,  
         detail={"error":"Empty request body"} 
        )

    for task in tasks:
        if task["id"]==id:
            if item.title is not None:
                if not item.title.strip():
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail={"error": "Title cannot be empty"}
                    )
                task["title"] = item.title.strip()
            
            if item.done is not None:
                task["done"] = item.done
                
            return task

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail={"error": f"Task {id} not found"}
    )

@app.delete("/tasks/{id}",status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(id:int):
    """Deletes the task with a given id from the list"""
    for task in tasks:
        if task["id"]==id:
            tasks.remove(task)
            return Response(status_code=status.HTTP_204_NO_CONTENT)

    raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error": f"Task {id} not found"}
        )