from validation import validate_enrollment
from results_page import show_results


def calculate_assessment(app, e):
    app.status.value = ""

    error, data = validate_enrollment(app)

    if error:
        app.status.value = "Please fill out all the blanks"
        app.page.update()
        return

    show_results(app, data)
