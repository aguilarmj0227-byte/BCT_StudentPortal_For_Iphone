import re
import flet as ft

from config import BORDER_COLOR

ERROR_COLOR = "#DC2626"


def get_field_error(app, field_name):
    field = app.field_map[field_name]
    value = (field.value or "").strip()

    required_fields = {
        "student_id": "Student ID Number is required.",
        "course": "Course / Program is required.",
        "last_name": "Last Name is required.",
        "first_name": "First Name is required.",
        "mi": "M.I. is required.",
    }

    if field_name in required_fields and not value:
        return required_fields[field_name]

    if field_name == "mi":
        if not re.fullmatch(r"[A-Za-z]\.?", value):
            return "Enter one letter only (e.g., A or A.)."

    elif field_name == "total_units":
        if not value:
            return "Total Units is required."

        try:
            units = int(value)
        except ValueError:
            return "Enter a valid whole number of units."

        if not 1 <= units <= 25:
            return "Units must be between 1 and 25."

    elif field_name == "lab_classes":
        if not value:
            return "Number of Laboratory is required."

        try:
            laboratory = int(value)
        except ValueError:
            return "Enter a valid whole number."

        if not 0 <= laboratory <= 5:
            return "Laboratory must be 0 to 5."

        try:
            units = int((app.total_units.value or "").strip())
            if laboratory > units:
                return "Laboratory cannot exceed total units."
        except ValueError:
            pass

    elif field_name == "hands_on":
        if not value:
            return "Number of Hands-on is required."

        try:
            hands_on = int(value)
        except ValueError:
            return "Enter a valid whole number."

        if not 0 <= hands_on <= 5:
            return "Hands-on must be 0 to 5."

        try:
            units = int((app.total_units.value or "").strip())
            if hands_on > units:
                return "Hands-on cannot exceed total units."
        except ValueError:
            pass

    elif field_name == "down_payment":
        if not value:
            return "Downpayment is required."

        try:
            downpayment = int(value)
        except ValueError:
            return "Enter a valid whole number."

        if downpayment < 3500:
            return "Minimum downpayment: ₱3,500."

    return None


def update_field_error(app, field_name, force=False):
    field = app.field_map[field_name]
    error = get_field_error(app, field_name)
    label = app.error_labels[field_name]

    if app.validation_attempted or force:
        label.value = error or ""
        label.visible = bool(error)
        field.error_text = None
        field.border_color = ERROR_COLOR if error else BORDER_COLOR
    else:
        field.border_color = BORDER_COLOR
        field.error_text = None
        label.value = ""
        label.visible = False

    return error


def handle_field_focus(app, field_name):
    if app.validation_attempted:
        update_field_error(app, field_name, force=True)
        app.page.update()


def handle_field_change(app, field_name):
    if app.validation_attempted:
        for name in app.field_map:
            update_field_error(app, name, force=True)
        app.page.update()


def validate_enrollment(app):
    app.validation_attempted = True
    errors = {}

    for field_name in app.field_map:
        error = update_field_error(app, field_name, force=True)
        if error:
            errors[field_name] = error

    if errors:
        app.page.update()
        return next(iter(errors.values())), None

    data = {
        "student_id": (app.student_id.value or "").strip(),
        "course": (app.course.value or "").strip(),
        "last_name": (app.last_name.value or "").strip(),
        "first_name": (app.first_name.value or "").strip(),
        "middle_initial": (app.mi.value or "").strip(),
        "units": int((app.total_units.value or "").strip()),
        "laboratory": int((app.lab_classes.value or "").strip()),
        "hands_on": int((app.hands_on.value or "").strip()),
        "down_payment": int((app.downpayment.value or "").strip()),
    }

    app.page.update()
    return None, data