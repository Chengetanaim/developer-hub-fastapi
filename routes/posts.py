from fastapi import APIRouter, Depends, HTTPException, Request, status
from database.connection import get_session
from models.posts import Post, PostUpdate
from typing import Optional, List
from sqlmodel import select

posts_router = APIRouter(tags=["Post"])

@posts_router.post("/new")
async def create_post(new_post:Post, session=Depends(get_session)) -> dict:
    session.add(new_post)
    session.commit()
    session.refresh(new_post)
    return {"message": "Event created successfully!"}    

@posts_router.get("/", response_model=List[Post])
async def retrieve_all_events(session=Depends(get_session)) -> Post:
    statement = select(Post)
    posts = session.exec(statement).all()
    return posts

@posts_router.get("/{id}", response_model=Post)
async def retrieve_post(id:int, session=Depends(get_session)) -> Post:
    post = session.get(Post, id)
    if post:
        return post
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post with suppied ID doesn't exist")

@posts_router.put("/edit/{id}", response_model=Post)
async def update_event(id:int,new_data:PostUpdate,session=Depends(get_session)) -> Post:
    post = session.get(Post,id)
    if post:
        post_data = new_data.dict(exclude_unset=True)
        for key, value in post_data.items():
            setattr(post,key,value)
        session.add(post)
        session.commit()
        session.refresh(post)
        return post
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post with supplied ID doesn't exist")

@posts_router.delete("/delete/{id}")
async def delete_event(id:int,session=Depends(get_session)) -> dict:
    post = session.get(Post, id)
    if post:
        session.delete(post)
        session.commit()
        return {"message": "Post deleted successfully"}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Event with supplied ID doesn't exist")