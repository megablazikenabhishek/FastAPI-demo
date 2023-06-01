from fastapi import FastAPI, Depends, status, Response, HTTPException
from typing import Optional, List, Dict
from schemas import BlogSchema, UserSchema
from models import Blog, User
from database import engine, get_db
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from fastapi.responses import HTMLResponse

Blog.base.metadata.create_all(bind=engine)

app = FastAPI()


@app.get("/", response_class=HTMLResponse, tags=["root"])
def index():
    return '''<h1>Blog API</h1>'''


@app.get("/blog", status_code=status.HTTP_200_OK, response_model=List[BlogSchema.showBlog], tags=["blogs"])
def blog(db: Session = Depends(get_db)):
    blogs = db.query(Blog.Blog).all()
    # print(blogs[0])
    return blogs


@app.post("/blog", status_code=status.HTTP_201_CREATED, tags=["blogs"])
def createBlog(req: BlogSchema.Blog, db: Session = Depends(get_db)):
    new_blog = Blog.Blog(title=req.title, body=req.body)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


@app.get("/blog/{id}", status_code=status.HTTP_200_OK, response_model=BlogSchema.showBlog, tags=["blogs"])
def show_blog_of_givenId(id: int, response: Response, db: Session = Depends(get_db)):
    blog = db.query(Blog.Blog).filter(Blog.Blog.id == id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"blog with id {id} not found")
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"data": f"blog with id {id} not found"}
    return blog


@app.delete("/blog/{id}", status_code=status.HTTP_204_NO_CONTENT, tags=["blogs"])
def delete_blog(id: int, db: Session = Depends(get_db)):
    blog = db.query(Blog.Blog).filter(Blog.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"blog with id {id} not found")

    blog.delete(synchronize_session=False)
    db.commit()
    return {"data": f"blog with id {id} deleted"}


@app.put("/blog/{id}", status_code=status.HTTP_202_ACCEPTED, tags=["blogs"])
def upadte_blo(id: int, req: BlogSchema.Blog, db: Session = Depends(get_db)):
    blog = db.query(Blog.Blog).filter(Blog.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"blog with id {id} not found")
    blog.update(req.dict())
    db.commit()
    # return the updated blog
    # print(blog)
    return {"data": blog.first()}


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@app.post("/user", response_model=UserSchema.showUser, status_code=status.HTTP_201_CREATED, tags=["users"])
def create_user(req: UserSchema.User, db: Session = Depends(get_db)):
    hashed_password = pwd_context.hash(req.password)
    new_user = User.User(name=req.name, email=req.email,
                         password=hashed_password)
    try:
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        print(new_user)
        return new_user
    except:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"email {req.email} already exists")


@app.get("/user/{id}", response_model=UserSchema.showUser, status_code=status.HTTP_200_OK, tags=["users"])
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(User.User).filter(User.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"user with id {id} not found")
    return user
