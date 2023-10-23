from typing import List, Optional
from fastapi import FastAPI
from database.connection import conn
from routes.posts import posts_router
import uvicorn 


app = FastAPI()
app.include_router(posts_router, prefix="/posts")

@app.on_event("startup")
def on_startup():
    conn()

@app.get('/')
async def index() -> dict:
    return {"message": "This is the home"}


# if __name__ == '__main__':
#     uvicorn.run("main:app", host="0.0.0.0", port=8080,reload=True)
