import flet as ft
from datetime import datetime
from models.grade import Grade
from models.student import Student
from database import get_session

class GradeView(ft.UserControl):
    def __init__(self):
        super().__init__()
        self.grades_table = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("Student")),
                ft.DataColumn(ft.Text("Subject")),
                ft.DataColumn(ft.Text("Score")),
                ft.DataColumn(ft.Text("Date")),
                ft.DataColumn(ft.Text("Notes")),
                ft.DataColumn(ft.Text("Actions")),
            ],
            rows=[]
        )
        
        # Form fields
        self.student_dropdown = ft.Dropdown(label="Student")
        self.subject = ft.TextField(label="Subject")
        self.score = ft.TextField(label="Score")
        self.notes = ft.TextField(label="Notes", multiline=True)
    
    def build(self):
        self.load_students()
        self.load_grades()
        return ft.Column([
            ft.Text("Grade Management", size=30, weight=ft.FontWeight.BOLD),
            ft.ElevatedButton(
                "Add Grade",
                on_click=self.show_grade_dialog
            ),
            self.grades_table
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
    
    def show_grade_dialog(self, e):
        def save_grade(e):
            session = next(get_session())
            grade = Grade(
                student_id=int(self.student_dropdown.value),
                subject=self.subject.value,
                score=float(self.score.value),
                notes=self.notes.value
            )
            session.add(grade)
            session.commit()
            self.load_grades()
            dialog.open = False
            self.page.update()

        dialog = ft.AlertDialog(
            title=ft.Text("Add Grade"),
            content=ft.Column([
                self.student_dropdown,
                self.subject,
                self.score,
                self.notes,
            ], tight=True),
            actions=[
                ft.TextButton("Cancel", on_click=lambda e: setattr(dialog, 'open', False)),
                ft.TextButton("Save", on_click=save_grade),
            ],
        )
        self.page.dialog = dialog
        dialog.open = True
        self.page.update()
    
    def load_grades(self):
        session = next(get_session())
        grades = (
            session.query(Grade, Student)
            .join(Student)
            .all()
        )
        
        self.grades_table.rows.clear()
        for grade, student in grades:
            self.grades_table.rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(f"{student.first_name} {student.last_name}")),
                        ft.DataCell(ft.Text(grade.subject)),
                        ft.DataCell(ft.Text(str(grade.score))),
                        ft.DataCell(ft.Text(grade.date.strftime("%Y-%m-%d"))),
                        ft.DataCell(ft.Text(grade.notes or "")),
                        ft.DataCell(
                            ft.Row([
                                ft.IconButton(
                                    ft.icons.EDIT,
                                    on_click=lambda e, g=grade: self.edit_grade(g)
                                ),
                                ft.IconButton(
                                    ft.icons.DELETE,
                                    on_click=lambda e, g=grade: self.delete_grade(g)
                                )
                            ])
                        )
                    ]
                )
            )
        self.update()
    
    def edit_grade(self, grade):
        # Pre-fill the form fields
        self.student_dropdown.value = str(grade.student_id)
        self.subject.value = grade.subject
        self.score.value = str(grade.score)
        self.notes.value = grade.notes or ""

        def save_changes(e):
            session = next(get_session())
            grade.subject = self.subject.value
            grade.score = float(self.score.value)
            grade.notes = self.notes.value
            session.merge(grade)
            session.commit()
            self.load_grades()
            dialog.open = False
            self.page.update()

        dialog = ft.AlertDialog(
            title=ft.Text("Edit Grade"),
            content=ft.Column([
                self.student_dropdown,
                self.subject,
                self.score,
                self.notes,
            ], tight=True),
            actions=[
                ft.TextButton("Cancel", on_click=lambda e: setattr(dialog, 'open', False)),
                ft.TextButton("Save", on_click=save_changes),
            ],
        )
        self.page.dialog = dialog
        dialog.open = True
        self.page.update()
    
    def delete_grade(self, grade):
        def confirm_delete(e):
            session = next(get_session())
            session.delete(grade)
            session.commit()
            self.load_grades()
            dialog.open = False
            self.page.update()

        dialog = ft.AlertDialog(
            title=ft.Text("Confirm Delete"),
            content=ft.Text("Are you sure you want to delete this grade?"),
            actions=[
                ft.TextButton("Cancel", on_click=lambda e: setattr(dialog, 'open', False)),
                ft.TextButton("Delete", on_click=confirm_delete),
            ],
        )
        self.page.dialog = dialog
        dialog.open = True