from pydantic import BaseModel


class User(BaseModel):
    name: str
    email: str
    password: str


class showUser(BaseModel):
    name: str
    email: str

    class Config:
        orm_mode = True
