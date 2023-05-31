from fastapi import FastAPI
from typing import Optional
from schemas import BlogSchema
from models import Blog
from database import engine

Blog.base.metadata.create_all(bind=engine)

app = FastAPI()


@app.get("/")
def index():
    return {
        "data": {
            "name": "Abhi",
            "age": 9
        }
    }


@app.get("/blog")
def blog(limit: int = 10, published: bool = True, sort: Optional[str] = None):
    return {"data": f"This are your {limit}, {published} blogs"}


@app.post("/blog")
def createBlog(req: BlogSchema.Blog):
    print(req)
    return req


@app.get("/blog/unpublished")
def unpublished():
    return {"data": "this are the unpublished blogs"}


@app.get("/blog/{id}")
def show(id: int):
    return {"data": id}


@app.get("/blog/{id}/comments")
def showComments(id: int):
    return {"data": f"comment of blog {id}"}
