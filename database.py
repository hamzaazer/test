from sqlmodel import SQLModel, create_engine, Session
import os

DATABASE_URL = "sqlite:///student_management.db"
engine = create_engine(DATABASE_URL)

def init_db():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session