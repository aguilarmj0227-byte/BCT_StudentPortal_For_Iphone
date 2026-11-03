import flet as ft


BURGUNDY = "#8F2638"
DARK_LABEL = "#334155"
MUTED_TEXT = "#475569"
INPUT_TEXT = "#1A202C"
BORDER_COLOR = "#222222",
DIVIDER_COLOR = "#CBD5E1"
CARD_BACKGROUND = "#F1F5F9"
WHITE = "#FFFFFF"


def setup_window(page: ft.Page):
    page.title = "BCT Student Portal"
    page.window.width = 520
    page.window.height = 850
    page.run_task(page.window.center)
    page.padding = 0
    page.spacing = 0
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
