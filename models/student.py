from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime

class Student(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    first_name: str
    last_name: str
    student_id: str = Field(unique=True)
    academic_year: int
    specialty: str
    class_name: str
    group: str
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)