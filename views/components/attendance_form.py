import flet as ft
from datetime import datetime
from models.attendance import Attendance
from utils.validation import validate_attendance_data
from utils.ui import create_error_dialog, show_snackbar
from utils.database import DatabaseManager

class AttendanceForm(ft.UserControl):
    def __init__(self, student_id: int, on_save=None, attendance=None):
        super().__init__()
        self.student_id = student_id
        self.on_save = on_save
        self.attendance = attendance
        
        self.date = ft.TextField(
            label="Date (YYYY-MM-DD)",
            value=attendance.date.strftime("%Y-%m-%d") if attendance else ""
        )
        self.status = ft.Dropdown(
            label="Status",
            options=[
                ft.dropdown.Option("Present"),
                ft.dropdown.Option("Absent"),
                ft.dropdown.Option("Late"),
            ],
            value=attendance.status if attendance else None
        )
        self.notes = ft.TextField(
            label="Notes",
            multiline=True,
            value=attendance.notes if attendance else ""
        )
    
    def build(self):
        return ft.Column([
            self.date,
            self.status,
            self.notes,
            ft.Row([
                ft.ElevatedButton(
                    "Save",
                    on_click=self.save_attendance
                )
            ])
        ], tight=True)
    
    def save_attendance(self, e):
        data = {
            'date': self.date.value,
            'status': self.status.value,
            'notes': self.notes.value
        }
        
        errors = validate_attendance_data(data)
        if errors:
            self.page.dialog = create_error_dialog(errors)
            self.page.dialog.open = True
            self.page.update()
            return
        
        try:
            attendance_data = {
                'student_id': self.student_id,
                'date': datetime.strptime(self.date.value, "%Y-%m-%d"),
                'status': self.status.value,
                'notes': self.notes.value
            }
            
            if self.attendance:
                for key, value in attendance_data.items():
                    setattr(self.attendance, key, value)
                DatabaseManager.update(self.attendance)
                show_snackbar(self.page, "Attendance updated successfully")
            else:
                attendance = Attendance(**attendance_data)
                DatabaseManager.create(attendance)
                show_snackbar(self.page, "Attendance marked successfully")
            
            if self.on_save:
                self.on_save()
        except Exception as e:
            self.page.dialog = create_error_dialog([str(e)])
            self.page.dialog.open = True
            self.page.update()