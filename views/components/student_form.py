import flet as ft
from models.student import Student
from utils.validation import validate_student_data
from utils.ui import create_error_dialog, show_snackbar
from utils.database import DatabaseManager

class StudentForm(ft.UserControl):
    def __init__(self, on_save=None, student=None):
        super().__init__()
        self.on_save = on_save
        self.student = student
        
        self.first_name = ft.TextField(
            label="First Name",
            value=student.first_name if student else ""
        )
        self.last_name = ft.TextField(
            label="Last Name",
            value=student.last_name if student else ""
        )
        self.student_id = ft.TextField(
            label="Student ID",
            value=student.student_id if student else ""
        )
        self.academic_year = ft.TextField(
            label="Academic Year",
            value=str(student.academic_year) if student else ""
        )
        self.specialty = ft.TextField(
            label="Specialty",
            value=student.specialty if student else ""
        )
        self.class_name = ft.TextField(
            label="Class",
            value=student.class_name if student else ""
        )
        self.group = ft.TextField(
            label="Group",
            value=student.group if student else ""
        )
    
    def build(self):
        return ft.Column([
            self.first_name,
            self.last_name,
            self.student_id,
            self.academic_year,
            self.specialty,
            self.class_name,
            self.group,
            ft.Row([
                ft.ElevatedButton(
                    "Save",
                    on_click=self.save_student
                )
            ])
        ], tight=True)
    
    def save_student(self, e):
        data = {
            'first_name': self.first_name.value,
            'last_name': self.last_name.value,
            'student_id': self.student_id.value,
            'academic_year': self.academic_year.value,
            'specialty': self.specialty.value,
            'class_name': self.class_name.value,
            'group': self.group.value
        }
        
        errors = validate_student_data(data)
        if errors:
            self.page.dialog = create_error_dialog(errors)
            self.page.dialog.open = True
            self.page.update()
            return
        
        try:
            if self.student:
                for key, value in data.items():
                    setattr(self.student, key, value)
                DatabaseManager.update(self.student)
                show_snackbar(self.page, "Student updated successfully")
            else:
                student = Student(**data)
                DatabaseManager.create(student)
                show_snackbar(self.page, "Student created successfully")
            
            if self.on_save:
                self.on_save()
        except Exception as e:
            self.page.dialog = create_error_dialog([str(e)])
            self.page.dialog.open = True
            self.page.update()