from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from config import MYSQL_URI

SQL_ALCHEMY_DATABASE_URL = MYSQL_URI

engine = create_engine(SQL_ALCHEMY_DATABASE_URL)

sessionLocal = sessionmaker(autocommit=False, bind=engine, autoflush=False)

base = declarative_base()


def get_db():
    db = sessionLocal()
    try:
        yield db
    finally:
        db.close()
