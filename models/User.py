from sqlalchemy import Row, Column, Integer, String
from database import base
from sqlalchemy.orm import relationship


class User(base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100))
    email = Column(String(100), unique=True)
    password = Column(String(200))

    blogs = relationship("Blog", back_populates="creator")
