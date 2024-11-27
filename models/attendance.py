from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime

class Attendance(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    student_id: int = Field(foreign_key="student.id")
    date: datetime
    status: str  # Present, Absent, Late
    notes: Optional[str] = None