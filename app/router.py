from fastapi import APIRouter, Request, status, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from .schemas import TodoSchema, TodoUpdateSchema

todo_router = APIRouter()


@todo_router.get("/list", response_description="Get 100 of todos")
async def list_todos(req: Request):
    todos = []
    for document in await req.app.mongodb["todos"].find().to_list(length=100):
        todos.append(document)
    return JSONResponse(content=todos, status_code=status.HTTP_200_OK)


@todo_router.post("/create", response_description="Create a todo")
async def create_todo(req: Request, todo_schema: TodoSchema):
    todo = jsonable_encoder(todo_schema)
    commit_todo = await req.app.mongodb["todos"].insert_one(todo)
    fetch_todo = await req.app.mongodb["todos"].find_one(
        {"_id": commit_todo.inserted_id}
    )
    return JSONResponse(
        content=fetch_todo,
        status_code=status.HTTP_201_CREATED
    )


@todo_router.put("/update/{todo_id}", response_description="Update a todo")
async def update_todo(req: Request, todo_id: str, todo: TodoUpdateSchema):
    if await req.app.mongodb["todos"].find_one({"_id": todo_id}) is None:
        raise HTTPException(
            detail={"response": "todo not found"},
            status_code=status.HTTP_404_NOT_FOUND
        )
    await req.app.mongodb["todos"].update_one(
        {"_id": todo_id},
        {"$set": todo.dict()}
    )
    return JSONResponse(
        content=await req.app.mongodb["todos"].find_one({"_id": todo_id}),
        status_code=status.HTTP_200_OK
    )


@todo_router.delete("/delete/{todo_id}", response_description="Delete a todo")
async def delete_todo(req: Request, todo_id: str):
    deleted_todo = await req.app.mongodb["todos"].delete_one({"_id": todo_id})
    if deleted_todo.deleted_count == 1:
        return JSONResponse(
            content={"response": f"todo {todo_id} was deleted"},
            status_code=status.HTTP_204_NO_CONTENT
        )
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="todo not found"
    )
