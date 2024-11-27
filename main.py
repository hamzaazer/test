import flet as ft
from database import init_db
from views.student_view import StudentView
from views.attendance_view import AttendanceView
from views.grade_view import GradeView

class StudentManagementSystem:
    def __init__(self):
        init_db()
        
    def main(self, page: ft.Page):
        page.title = "Student Management System"
        page.theme_mode = ft.ThemeMode.LIGHT
        page.padding = 20
        
        def route_change(route):
            page.views.clear()
            page.views.append(
                ft.View(
                    "/",
                    [
                        ft.AppBar(
                            title=ft.Text("Student Management System"),
                            bgcolor=ft.colors.BLUE,
                            center_title=True,
                        ),
                        ft.NavigationRail(
                            selected_index=0,
                            label_type=ft.NavigationRailLabelType.ALL,
                            destinations=[
                                ft.NavigationRailDestination(
                                    icon=ft.icons.PEOPLE,
                                    label="Students"
                                ),
                                ft.NavigationRailDestination(
                                    icon=ft.icons.CALENDAR_TODAY,
                                    label="Attendance"
                                ),
                                ft.NavigationRailDestination(
                                    icon=ft.icons.GRADE,
                                    label="Grades"
                                ),
                            ],
                            on_change=lambda e: switch_view(e.control.selected_index)
                        ),
                        ft.VerticalDivider(width=1),
                        ft.Container(
                            content=StudentView(),
                            expand=True,
                            padding=20
                        )
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.START
                )
            )
            page.update()
        
        def switch_view(index):
            content = None
            if index == 0:
                content = StudentView()
            elif index == 1:
                content = AttendanceView()
            elif index == 2:
                content = GradeView()
            
            page.views[0].controls[-1].content = content
            page.update()
        
        page.on_route_change = route_change
        page.go('/')

if __name__ == '__main__':
    app = StudentManagementSystem()
    ft.app(target=app.main)