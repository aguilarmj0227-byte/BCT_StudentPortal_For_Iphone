import flet as ft

from config import setup_window
from enrollment_page import build_enrollment_page, clear_fields
from assessment import calculate_assessment
from results_page import show_results


class BCTEnrollmentApp:
    def __init__(self, page: ft.Page):
        self.page = page
        setup_window(self.page)
        self.build_ui()

        self.records = []
        self.calculation_history = []

    def build_ui(self):
        build_enrollment_page(self)

    def calculate_assessment(self, e):
        calculate_assessment(self, e)

    def clear_fields(self, e):
        clear_fields(self, e)

    def show_enrollment_page(self, e=None):
        show_results(self)


if __name__ == "__main__":
    ft.run(lambda page: BCTEnrollmentApp(page))
