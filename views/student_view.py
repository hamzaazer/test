import flet as ft
from typing import Optional
from models.student import Student
from database import get_session

class StudentView(ft.UserControl):
    def __init__(self):
        super().__init__()
        self.students_table = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("ID")),
                ft.DataColumn(ft.Text("Name")),
                ft.DataColumn(ft.Text("Year")),
                ft.DataColumn(ft.Text("Class")),
                ft.DataColumn(ft.Text("Group")),
                ft.DataColumn(ft.Text("Actions")),
            ],
            rows=[]
        )
        
        # Form fields
        self.first_name = ft.TextField(label="First Name")
        self.last_name = ft.TextField(label="Last Name")
        self.student_id = ft.TextField(label="Student ID")
        self.academic_year = ft.TextField(label="Academic Year")
        self.specialty = ft.TextField(label="Specialty")
        self.class_name = ft.TextField(label="Class")
        self.group = ft.TextField(label="Group")
        
    def build(self):
        self.load_students()
        return ft.Column([
            ft.Text("Students Management", size=30, weight=ft.FontWeight.BOLD),
            ft.ElevatedButton(
                "Add New Student",
                on_click=self.show_add_dialog
            ),
            self.students_table
        ])
    
    def show_add_dialog(self, e):
        def save_student(e):
            session = next(get_session())
            student = Student(
                first_name=self.first_name.value,
                last_name=self.last_name.value,
                student_id=self.student_id.value,
                academic_year=int(self.academic_year.value),
                specialty=self.specialty.value,
                class_name=self.class_name.value,
                group=self.group.value
            )
            session.add(student)
            session.commit()
            self.load_students()
            dialog.open = False
            self.page.update()

        dialog = ft.AlertDialog(
            title=ft.Text("Add New Student"),
            content=ft.Column([
                self.first_name,
                self.last_name,
                self.student_id,
                self.academic_year,
                self.specialty,
                self.class_name,
                self.group,
            ], tight=True),
            actions=[
                ft.TextButton("Cancel", on_click=lambda e: setattr(dialog, 'open', False)),
                ft.TextButton("Save", on_click=save_student),
            ],
        )
        self.page.dialog = dialog
        dialog.open = True
        self.page.update()
    
    def edit_student(self, student):
        # Pre-fill the form fields
        self.first_name.value = student.first_name
        self.last_name.value = student.last_name
        self.student_id.value = student.student_id
        self.academic_year.value = str(student.academic_year)
        self.specialty.value = student.specialty
        self.class_name.value = student.class_name
        self.group.value = student.group

        def save_changes(e):
            session = next(get_session())
            student.first_name = self.first_name.value
            student.last_name = self.last_name.value
            student.student_id = self.student_id.value
            student.academic_year = int(self.academic_year.value)
            student.specialty = self.specialty.value
            student.class_name = self.class_name.value
            student.group = self.group.value
            session.merge(student)
            session.commit()
            self.load_students()
            dialog.open = False
            self.page.update()

        dialog = ft.AlertDialog(
            title=ft.Text("Edit Student"),
            content=ft.Column([
                self.first_name,
                self.last_name,
                self.student_id,
                self.academic_year,
                self.specialty,
                self.class_name,
                self.group,
            ], tight=True),
            actions=[
                ft.TextButton("Cancel", on_click=lambda e: setattr(dialog, 'open', False)),
                ft.TextButton("Save", on_click=save_changes),
            ],
        )
        self.page.dialog = dialog
        dialog.open = True
        self.page.update()

    def delete_student(self, student):
        def confirm_delete(e):
            session = next(get_session())
            session.delete(student)
            session.commit()
            self.load_students()
            dialog.open = False
            self.page.update()

        dialog = ft.AlertDialog(
            title=ft.Text("Confirm Delete"),
            content=ft.Text(f"Are you sure you want to delete {student.first_name} {student.last_name}?"),
            actions=[
                ft.TextButton("Cancel", on_click=lambda e: setattr(dialog, 'open', False)),
                ft.TextButton("Delete", on_click=confirm_delete),
            ],
        )
        self.page.dialog = dialog
        dialog.open = True
        self.page.update()
    
    def load_students(self):
        session = next(get_session())
        students = session.query(Student).all()
        
        self.students_table.rows.clear()
        for student in students:
            self.students_table.rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(student.student_id)),
                        ft.DataCell(ft.Text(f"{student.first_name} {student.last_name}")),
                        ft.DataCell(ft.Text(str(student.academic_year))),
                        ft.DataCell(ft.Text(student.class_name)),
                        ft.DataCell(ft.Text(student.group)),
                        ft.DataCell(
                            ft.Row([
                                ft.IconButton(
                                    ft.icons.EDIT,
                                    on_click=lambda e, s=student: self.edit_student(s)
                                ),
                                ft.IconButton(
                                    ft.icons.DELETE,
                                    on_click=lambda e, s=student: self.delete_student(s)
                                )
                            ])
                        )
                    ]
                )
            )
        self.update()