from fastapi import FastAPI, status, Body, HTTPException, Path
from pydantic import BaseModel
from typing import List

app = FastAPI()

users = []


class User(BaseModel):
    id: int
    username: str
    age: int


@app.get("/users")
async def get_all_users():
    return users


@app.post("/user/{username}/{age}")
async def create_user(username: str = Path(min_length=5, max_length=20, description="Enter username")
                      , age: int = Path(ge=18, le=120, description="Enter age")) -> User:
     if not users:
        next_id = 1
    else:
        next_id = max(user.id for user in users) + 1
    new_user = User(id=next_id, username=username, age=age)
    users.append(new_user)
    return new_user


@app.put("/user/{user_id}/{username}/{age}")
async def update_user(user_id: int = Path(ge=1, le=100, description="Enter User ID")
                      , username: str = Path(min_length=5, max_length=20, description="Enter username")
                      , age: int = Path(ge=18, le=120, description="Enter age")) ->User:
    for user in users:
        if user.id == user_id:
            user.username = username
            user.age = age
            return user
    raise HTTPException(status_code=404, detail=f"User with id {user_id} not found")


@app.delete("/user/{user_id}")
async def delete_user(user_id: int) -> User:
    for i, user in enumerate(users):
        if user.id == user_id:
            removed_user = users.pop(i)
            return removed_user
    raise HTTPException(status_code=404, detail=f"User with id {user_id} not found")
