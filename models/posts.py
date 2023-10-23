from sqlmodel import JSON, SQLModel, Field, Column
from typing import Optional, List


class Post(SQLModel, table=True):
    id: int=Field(default=None, primary_key=True)
    title: str
    content: str

class PostUpdate(SQLModel):
    title: Optional[str]
    content: Optional[str]