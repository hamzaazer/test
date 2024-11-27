from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime

class Grade(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    student_id: int = Field(foreign_key="student.id")
    subject: str
    score: float
    date: datetime = Field(default_factory=datetime.now)
    notes: Optional[str] = None