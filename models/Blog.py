from database import base
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey


class Blog(base):
    __tablename__ = "blogs"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), nullable=False)
    body = Column(String(100), nullable=False)
