from pydantic import BaseModel
from . import UserSchema


class Blog(BaseModel):
    title: str
    body: str


class showBlog(BaseModel):
    title: str
    body: str
    print(UserSchema.showUser)
    creator: UserSchema.showUser

    class Config:
        orm_mode = True
