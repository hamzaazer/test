import flet as ft
from datetime import datetime
from models.attendance import Attendance
from models.student import Student
from database import get_session

class AttendanceView(ft.UserControl):
    def __init__(self):
        super().__init__()
        self.attendance_table = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("Student")),
                ft.DataColumn(ft.Text("Date")),
                ft.DataColumn(ft.Text("Status")),
                ft.DataColumn(ft.Text("Notes")),
                ft.DataColumn(ft.Text("Actions")),
            ],
            rows=[]
        )
        
        # Form fields
        self.student_dropdown = ft.Dropdown(label="Student")
        self.date_picker = ft.TextField(label="Date (YYYY-MM-DD)")
        self.status_dropdown = ft.Dropdown(
            label="Status",
            options=[
                ft.dropdown.Option("Present"),
                ft.dropdown.Option("Absent"),
                ft.dropdown.Option("Late"),
            ]
        )
        self.notes = ft.TextField(label="Notes", multiline=True)
    
    def build(self):
        self.load_students()
        self.load_attendance()
        return ft.Column([
            ft.Text("Attendance Management", size=30, weight=ft.FontWeight.BOLD),
            ft.ElevatedButton(
                "Mark Attendance",
                on_click=self.show_attendance_dialog
            ),
            self.attendance_table
        ])
    
    def load_students(self):
        session = next(get_session())
        students = session.query(Student).all()
        self.student_dropdown.options = [
            ft.dropdown.Option(
                key=str(student.id),
                text=f"{student.first_name} {student.last_name}"
            ) for student in students
        ]
    
    def show_attendance_dialog(self, e):
        def save_attendance(e):
            session = next(get_session())
            attendance = Attendance(
                student_id=int(self.student_dropdown.value),
                date=datetime.strptime(self.date_picker.value, "%Y-%m-%d"),
                status=self.status_dropdown.value,
                notes=self.notes.value
            )
            session.add(attendance)
            session.commit()
            self.load_attendance()
            dialog.open = False
            self.page.update()

        dialog = ft.AlertDialog(
            title=ft.Text("Mark Attendance"),
            content=ft.Column([
                self.student_dropdown,
                self.date_picker,
                self.status_dropdown,
                self.notes,
            ], tight=True),
            actions=[
                ft.TextButton("Cancel", on_click=lambda e: setattr(dialog, 'open', False)),
                ft.TextButton("Save", on_click=save_attendance),
            ],
        )
        self.page.dialog = dialog
        dialog.open = True
        self.page.update()
    
    def load_attendance(self):
        session = next(get_session())
        attendance_records = (
            session.query(Attendance, Student)
            .join(Student)
            .all()
        )
        
        self.attendance_table.rows.clear()
        for attendance, student in attendance_records:
            self.attendance_table.rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(f"{student.first_name} {student.last_name}")),
                        ft.DataCell(ft.Text(attendance.date.strftime("%Y-%m-%d"))),
                        ft.DataCell(ft.Text(attendance.status)),
                        ft.DataCell(ft.Text(attendance.notes or "")),
                        ft.DataCell(
                            ft.IconButton(
                                ft.icons.DELETE,
                                on_click=lambda e, a=attendance: self.delete_attendance(a)
                            )
                        )
                    ]
                )
            )
        self.update()
    
    def delete_attendance(self, attendance):
        def confirm_delete(e):
            session = next(get_session())
            session.delete(attendance)
            session.commit()
            self.load_attendance()
            dialog.open = False
            self.page.update()

        dialog = ft.AlertDialog(
            title=ft.Text("Confirm Delete"),
            content=ft.Text("Are you sure you want to delete this attendance record?"),
            actions=[
                ft.TextButton("Cancel", on_click=lambda e: setattr(dialog, 'open', False)),
                ft.TextButton("Delete", on_click=confirm_delete),
            ],
        )
        self.page.dialog = dialog
        dialog.open = True
        self.page.update()