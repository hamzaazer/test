import flet as ft
from typing import Callable, List

def create_error_dialog(errors: List[str]) -> ft.AlertDialog:
    return ft.AlertDialog(
        title=ft.Text("Error"),
        content=ft.Column([ft.Text(error) for error in errors]),
        actions=[
            ft.TextButton("OK", on_click=lambda e: setattr(e.control.page.dialog, 'open', False))
        ]
    )

def create_confirmation_dialog(
    title: str,
    content: str,
    on_confirm: Callable,
    on_cancel: Callable = None
) -> ft.AlertDialog:
    return ft.AlertDialog(
        title=ft.Text(title),
        content=ft.Text(content),
        actions=[
            ft.TextButton("Cancel", on_click=on_cancel or (lambda e: setattr(e.control.page.dialog, 'open', False))),
            ft.TextButton("Confirm", on_click=on_confirm)
        ]
    )

def show_snackbar(page: ft.Page, message: str) -> None:
    page.show_snackbar(
        ft.SnackBar(
            content=ft.Text(message),
            action="OK",
            action_color=ft.colors.BLUE
        )
    )