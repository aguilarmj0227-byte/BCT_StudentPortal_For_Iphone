
import flet as ft

from validation import handle_field_focus, handle_field_change

from config import (
    BURGUNDY,
    DARK_LABEL,
    MUTED_TEXT,
    INPUT_TEXT,
    BORDER_COLOR,
    DIVIDER_COLOR,
    CARD_BACKGROUND,
    WHITE,
)


# ==========================================
# ENROLLMENT PAGE
# ==========================================

def build_enrollment_page(app):
    soft_dark_color = DARK_LABEL
    input_text_style = ft.TextStyle(color=INPUT_TEXT)

    app.status = ft.Text(size=13, color="#DC2626")
    app.validation_attempted = False
    app.result_area = ft.Column(spacing=12, visible=False)

    def create_field(label, expand=None, numeric=False):
        return ft.TextField(
            label=label,
            label_style=ft.TextStyle(
                size=12,
                color=soft_dark_color,
                weight=ft.FontWeight.W_600,
            ),
            text_style=input_text_style,
            border_radius=8,
            border_color=BORDER_COLOR,
            expand=expand,
            text_size=15,
            content_padding=12,
            keyboard_type=(
                ft.KeyboardType.NUMBER if numeric else ft.KeyboardType.TEXT
            ),
            bgcolor=WHITE,
        )

    app.student_id = create_field("Student ID Number")
    app.course = create_field("Course / Program")
    app.last_name = create_field("Last Name", expand=4)
    app.first_name = create_field("First Name", expand=4)
    app.mi = create_field("M.I.", expand=2)
    app.total_units = create_field(
        "Total Units (1-25)", expand=1, numeric=True
    )
    app.lab_classes = create_field(
        "No. of Laboratory", expand=1, numeric=True
    )
    app.hands_on = create_field(
        "No. of Hands-on", expand=1, numeric=True
    )
    app.downpayment = create_field(
        "Downpayment", expand=1, numeric=True
    )

    # PAGE FUNCTION CONNECTIONS
    app.show_how_to_use = lambda e: show_how_to_use(app, e)
    app.show_about_app = lambda e: show_about_app(app, e)
    app.show_records = lambda e: show_records(app, e)

    # HEADER
    header = ft.Container(
        content=ft.Row(
            controls=[
                ft.Image(
                    src="bct_logo.png",
                    width=65,
                    height=65,
                    fit=ft.BoxFit.CONTAIN,
                ),
                ft.Column(
                    controls=[
                        ft.Text(
                            "BAGUIO COLLEGE OF\nTECHNOLOGY",
                            size=18,
                            weight=ft.FontWeight.BOLD,
                            color=BURGUNDY,
                            style=ft.TextStyle(letter_spacing=0.5),
                        ),
                        ft.Text(
                            "ENROLLMENT & ASSESSMENT PORTAL",
                            size=10,
                            weight=ft.FontWeight.W_600,
                            color=MUTED_TEXT,
                            style=ft.TextStyle(letter_spacing=1),
                        ),
                    ],
                    spacing=2,
                    expand=True,
                ),
                ft.PopupMenuButton(
                    icon=ft.Icons.MENU_OUTLINED,
                    icon_size=22,
                    icon_color=MUTED_TEXT,
                    tooltip="Settings",
                    menu_position=ft.PopupMenuPosition.UNDER,
                    items=[
                        ft.PopupMenuItem(
                            content=ft.Text("How to use", size=12),
                            icon=ft.Icons.HELP_OUTLINE,
                            on_click=app.show_how_to_use,
                        ),
                        ft.PopupMenuItem(
                            content=ft.Text("Records", size=12),
                            icon=ft.Icons.HISTORY_OUTLINED,
                            on_click=app.show_records,
                        ),
                        ft.PopupMenuItem(
                            content=ft.Text("About this app", size=12),
                            icon=ft.Icons.ACCOUNT_CIRCLE_OUTLINED,
                            on_click=app.show_about_app,
                        ),
                        ft.PopupMenuItem(
                            content=ft.Text("Exit", size=12),
                            icon=ft.Icons.EXIT_TO_APP_OUTLINED,
                            on_click=lambda e: exit_application(app, e),
                        ),
                    ],
                ),
            ],
            spacing=12,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        padding=ft.Padding(20, 24, 20, 20),
    )

    divider = ft.Container(
        content=ft.Divider(height=1, color=DIVIDER_COLOR),
        padding=ft.Padding(20, 0, 20, 10),
    )

    # FIELD MAP
    app.field_map = {
        "student_id": app.student_id,
        "course": app.course,
        "last_name": app.last_name,
        "first_name": app.first_name,
        "mi": app.mi,
        "total_units": app.total_units,
        "lab_classes": app.lab_classes,
        "hands_on": app.hands_on,
        "down_payment": app.downpayment,
    }

    app.error_labels = {}
    app.field_controls = {}

    for field_name, field in app.field_map.items():
        error_label = ft.Text(
            "",
            color="#DC2626",
            size=11,
            visible=False,
        )

        app.error_labels[field_name] = error_label

        app.field_controls[field_name] = ft.Column(
            controls=[field, error_label],
            spacing=2,
            tight=True,
            expand=getattr(field, "expand", None) or False,
        )

        field.on_focus = (
            lambda e, name=field_name: handle_field_focus(app, name)
        )

        field.on_change = (
            lambda e, name=field_name: handle_field_change(app, name)
        )

    # ENROLLMENT FORM
    form_fields = ft.Column(
        controls=[
            ft.Text(
                "STUDENT IDENTITY & ACADEMIC PROFILE",
                size=11,
                weight=ft.FontWeight.BOLD,
                color=soft_dark_color,
                style=ft.TextStyle(letter_spacing=1),
            ),

            app.field_controls["student_id"],
            app.field_controls["course"],

            ft.Container(height=8),

            ft.Text(
                "PERSONAL INFORMATION",
                size=11,
                weight=ft.FontWeight.BOLD,
                color=soft_dark_color,
                style=ft.TextStyle(letter_spacing=1),
            ),

            ft.Row(
                controls=[
                    app.field_controls["last_name"],
                    app.field_controls["first_name"],
                    app.field_controls["mi"],
                ],
                spacing=10,
                vertical_alignment=ft.CrossAxisAlignment.START,
            ),

            ft.Container(height=8),

            ft.Text(
                "ACADEMIC LOAD & LABORATORY UNITS",
                size=11,
                weight=ft.FontWeight.BOLD,
                color=soft_dark_color,
                style=ft.TextStyle(letter_spacing=1),
            ),

            ft.Column(
                controls=[
                    ft.Row(
                        controls=[
                            app.field_controls["total_units"],
                            app.field_controls["down_payment"],
                        ],
                        spacing=10,
                        vertical_alignment=ft.CrossAxisAlignment.START,
                    ),

                    ft.Row(
                        controls=[
                            app.field_controls["lab_classes"],
                            app.field_controls["hands_on"],
                        ],
                        spacing=10,
                        vertical_alignment=ft.CrossAxisAlignment.START,
                    ),
                ],
                spacing=10,
            ),

            ft.Container(height=15),

            app.status,

            ft.Button(
                "Calculate Assessment & Submit",
                bgcolor=BURGUNDY,
                color="white",
                height=48,
                style=ft.ButtonStyle(
                    shape=ft.RoundedRectangleBorder(radius=8),
                ),
                width=float("inf"),
                on_click=app.calculate_assessment,
            ),

            ft.Button(
                "Clear Fields",
                bgcolor=BURGUNDY,
                color="white",
                height=48,
                style=ft.ButtonStyle(
                    shape=ft.RoundedRectangleBorder(radius=8),
                ),
                width=float("inf"),
                on_click=app.clear_fields,
            ),
        ],
        spacing=12,
    )

    # ENROLLMENT CARD
    portal_card = ft.Container(
        content=ft.Column(
            controls=[
                header,
                divider,
                ft.Container(
                    content=form_fields,
                    padding=ft.Padding(24, 0, 24, 28),
                ),
            ],
            scroll=ft.ScrollMode.ADAPTIVE,
            tight=True,
        ),
        bgcolor=CARD_BACKGROUND,
        border_radius=ft.BorderRadius(16, 16, 16, 16),
        width=460,
        height=740,
        shadow=ft.BoxShadow(
            blur_radius=20,
            color="#1A000000",
            offset=ft.Offset(0, 4),
        ),
    )

    # BACKGROUND
    background_layout = ft.Container(
        image=ft.DecorationImage(
            src="background.png",
            fit=ft.BoxFit.COVER,
        ),
        expand=True,
        width=float("inf"),
        height=float("inf"),
        content=portal_card,
        alignment=ft.Alignment(0, 0),
    )

    app.page.controls.clear()
    app.page.add(background_layout)
    app.page.update()


# ==========================================
# CLEAR FIELDS FUNCTION
# ==========================================

def clear_fields(app, e=None):
    app.student_id.value = ""
    app.course.value = ""
    app.last_name.value = ""
    app.first_name.value = ""
    app.mi.value = ""
    app.total_units.value = ""
    app.lab_classes.value = ""
    app.hands_on.value = ""
    app.downpayment.value = ""

    app.status.value = ""
    app.result_area.visible = False
    app.validation_attempted = False

    for field_name, field in app.field_map.items():
        field.error_text = None
        field.border_color = BORDER_COLOR

        app.error_labels[field_name].value = ""
        app.error_labels[field_name].visible = False

    app.page.update()


# ==========================================
# RECORDS PAGE
# ==========================================

def show_records(app, e=None):
    app.page.controls.clear()

    # FEE ROW
    def fee_row(label, value):
        return ft.Row(
            controls=[
                ft.Text(
                    label,
                    size=12,
                    color="#222222",
                    expand=True,
                ),
                ft.Text(
                    f"₱{value:,.2f}",
                    size=12,
                    color="#222222",
                    weight=ft.FontWeight.BOLD,
                ),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        )

    # CREATE RECORD CARD
    def create_record_card(record, index):
        return ft.Container(
            content=ft.Column(
                controls=[
                    ft.Text(
                        f"ENROLLMENT RECORD #{index}",
                        size=14,
                        weight=ft.FontWeight.BOLD,
                        color=BURGUNDY,
                    ),
                    ft.Text(
                        f"Date: {record['date']}",
                        size=11,
                        color=MUTED_TEXT,
                    ),
                    ft.Divider(color=DIVIDER_COLOR),

                    ft.Text(
                        "STUDENT INFORMATION",
                        size=12,
                        weight=ft.FontWeight.BOLD,
                        color=BURGUNDY,
                    ),
                    ft.Text(
                        f"Student ID: {record['student_id']}",
                        size=12,
                        color=DARK_LABEL,
                    ),
                    ft.Text(
                        f"Name: {record['full_name']}",
                        size=12,
                        color=DARK_LABEL,
                    ),
                    ft.Text(
                        f"Course: {record['course']}",
                        size=12,
                        color=DARK_LABEL,
                    ),

                    ft.Divider(color=DIVIDER_COLOR),

                    ft.Text(
                        "ACADEMIC LOAD",
                        size=12,
                        weight=ft.FontWeight.BOLD,
                        color=BURGUNDY,
                    ),
                    ft.Text(
                        f"Total Units: {record['total_units']}",
                        size=12,
                        color=DARK_LABEL,
                    ),
                    ft.Text(
                        f"Laboratory: {record['laboratory']}",
                        size=12,
                        color=DARK_LABEL,
                    ),
                    ft.Text(
                        f"Hands-on: {record['hands_on']}",
                        size=12,
                        color=DARK_LABEL,
                    ),

                    ft.Divider(color=DIVIDER_COLOR),

                    ft.Text(
                        "ASSESSMENT BREAKDOWN",
                        size=12,
                        weight=ft.FontWeight.BOLD,
                        color=BURGUNDY,
                    ),

                    fee_row("Tuition", record["units_tuition"]),
                    fee_row(
                        "Laboratory Fee",
                        record["laboratory_tuition"],
                    ),
                    fee_row(
                        "Hands-on Fee",
                        record["handson_tuition"],
                    ),

                    *[
                        fee_row(label, amount)
                        for label, amount in record["miscellaneous_fees"]
                    ],

                    ft.Divider(color=DIVIDER_COLOR),

                    fee_row(
                        "Total Miscellaneous Fees",
                        record["miscellaneous_total"],
                    ),
                    fee_row(
                        "TOTAL ASSESSMENT",
                        record["total_assessment"],
                    ),

                    ft.Divider(color=DIVIDER_COLOR),

                    ft.Text(
                        "PAYMENT SUMMARY",
                        size=12,
                        weight=ft.FontWeight.BOLD,
                        color=BURGUNDY,
                    ),
                    fee_row("Downpayment", record["downpayment"]),
                    fee_row(
                        "Remaining Balance",
                        record["remaining_balance"],
                    ),
                    fee_row(
                        "Exam Computation",
                        record["exam_computation"],
                    ),
                ],
                spacing=7,
            ),
            padding=15,
            bgcolor=WHITE,
            border_radius=12,
        )

    # SAVED ENROLLMENT RECORDS
    records = getattr(app, "records", [])
    history = getattr(app, "calculation_history", [])

    saved_records = [
        create_record_card(record, index)
        for index, record in enumerate(records, start=1)
    ]

    # CALCULATION HISTORY
    history_items = []

    for index, item in enumerate(history, start=1):
        history_items.append(
            ft.Container(
                content=ft.Column(
                    controls=[
                        ft.Text(
                            f"Calculation #{index}",
                            size=13,
                            weight=ft.FontWeight.BOLD,
                            color=BURGUNDY,
                        ),
                        ft.Text(
                            f"Student: {item['full_name']}",
                            size=12,
                            color=DARK_LABEL,
                        ),
                        ft.Text(
                            f"Student ID: {item['student_id']}",
                            size=12,
                            color=DARK_LABEL,
                        ),
                        ft.Text(
                            f"Total Assessment: "
                            f"₱{item['total_assessment']:,.2f}",
                            size=12,
                            weight=ft.FontWeight.BOLD,
                            color=DARK_LABEL,
                        ),
                        ft.Text(
                            f"Date: {item['date']}",
                            size=11,
                            color=MUTED_TEXT,
                        ),
                    ],
                    spacing=6,
                ),
                padding=12,
                bgcolor=WHITE,
                border_radius=10,
            )
        )

    # RECORDS CONTENT
    records_content = ft.Column(
        controls=[
            ft.Text(
                "SAVED ENROLLMENT RECORDS",
                size=14,
                weight=ft.FontWeight.BOLD,
                color=BURGUNDY,
            ),

            *(
                saved_records
                if saved_records
                else [
                    ft.Text(
                        "No saved enrollment records yet.",
                        size=12,
                        color=MUTED_TEXT,
                    )
                ]
            ),

            ft.Container(height=10),

            ft.Text(
                "CALCULATION HISTORY",
                size=14,
                weight=ft.FontWeight.BOLD,
                color=BURGUNDY,
            ),

            *(
                history_items
                if history_items
                else [
                    ft.Text(
                        "No calculation history yet.",
                        size=12,
                        color=MUTED_TEXT,
                    )
                ]
            ),
        ],
        spacing=12,
        scroll=ft.ScrollMode.AUTO,
        expand=True,
    )

    # RECORDS HEADER
    records_header = ft.Row(
        controls=[
            ft.IconButton(
                icon=ft.Icons.ARROW_BACK,
                icon_color=BURGUNDY,
                tooltip="Back to Enrollment",
                on_click=lambda e: build_enrollment_page(app),
            ),
            ft.Icon(
                ft.Icons.HISTORY_OUTLINED,
                color=BURGUNDY,
                size=22,
            ),
            ft.Text(
                "RECORDS",
                size=20,
                weight=ft.FontWeight.BOLD,
                color=BURGUNDY,
            ),
        ],
        spacing=5,
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
    )

    # RECORDS CARD
    records_page = ft.Container(
        content=ft.Column(
            controls=[
                records_header,
                ft.Divider(color=DIVIDER_COLOR),

                ft.Text(
                    "Enrollment Records & Calculation History",
                    size=17,
                    weight=ft.FontWeight.BOLD,
                    color=BURGUNDY,
                ),

                ft.Text(
                    "View saved student information and previous "
                    "assessment calculations.",
                    size=12,
                    color=MUTED_TEXT,
                ),

                records_content,
            ],
            spacing=12,
            expand=True,
        ),
        bgcolor=CARD_BACKGROUND,
        border_radius=16,
        padding=24,
        width=460,
        height=740,
        shadow=ft.BoxShadow(
            blur_radius=20,
            color="#1A000000",
            offset=ft.Offset(0, 4),
        ),
    )

    # BACKGROUND
    background_layout = ft.Container(
        image=ft.DecorationImage(
            src="background.png",
            fit=ft.BoxFit.COVER,
        ),
        expand=True,
        width=float("inf"),
        height=float("inf"),
        content=records_page,
        alignment=ft.Alignment(0, 0),
    )

    app.page.add(background_layout)
    app.page.update()

# ==========================================
# EXIT APPLICATION FUNCTION
# ==========================================

async def exit_application_async(app):
    if app.page.platform == ft.PagePlatform.ANDROID:
        await ft.SystemNavigator.pop()
    else:
        await app.page.window.close()


def exit_application(app, e=None):
    app.page.run_task(exit_application_async, app)

# ==========================================
# ABOUT THIS APP PAGE
# ==========================================

def show_about_app(app, e=None):
    app.page.controls.clear()

    # HEADER
    about_header = ft.Row(
        controls=[
            ft.IconButton(
                icon=ft.Icons.ARROW_BACK,
                icon_color=BURGUNDY,
                on_click=lambda e: build_enrollment_page(app),
                tooltip="Back to Enrollment",
            ),
            ft.Row(
                controls=[
                    ft.Icon(
                        ft.Icons.INFO_OUTLINE,
                        color=BURGUNDY,
                        size=24,
                    ),
                    ft.Text(
                        "ABOUT THIS APP",
                        size=20,
                        weight=ft.FontWeight.BOLD,
                        color=BURGUNDY,
                    ),
                ],
                spacing=5,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            ),
        ],
        spacing=5,
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
    )

    # APP INFORMATION
    app_information = ft.Column(
        controls=[
            ft.Text(
                "BAGUIO COLLEGE OF TECHNOLOGY",
                size=16,
                weight=ft.FontWeight.BOLD,
                color=BURGUNDY,
                text_align=ft.TextAlign.CENTER,
            ),

            ft.Text(
                "ENROLLMENT & ASSESSMENT PORTAL",
                size=13,
                weight=ft.FontWeight.W_600,
                color=MUTED_TEXT,
                text_align=ft.TextAlign.CENTER,
            ),

            ft.Container(height=10),

            ft.Text(
                "About the Application",
                size=15,
                weight=ft.FontWeight.BOLD,
                color=BURGUNDY,
            ),

            ft.Text(
                "The BCT Enrollment & Assessment Portal is an "
                "application designed to help students calculate "
                "and review their estimated enrollment fees. "
                "It provides an organized way to enter student "
                "information, academic units, and payment details "
                "to generate an assessment.",
                size=13,
                color=DARK_LABEL,
                text_align=ft.TextAlign.JUSTIFY,
            ),

            ft.Divider(color=DIVIDER_COLOR),

            ft.Text(
                "APP DETAILS",
                size=15,
                weight=ft.FontWeight.BOLD,
                color=BURGUNDY,
            ),

            ft.Text(
                "Application Name: BCT Enrollment & Assessment Portal",
                size=13,
                color=DARK_LABEL,
            ),

            ft.Text(
                "Institution: Baguio College of Technology",
                size=13,
                color=DARK_LABEL,
            ),

            ft.Text(
                "Application Type: Enrollment Assessment Calculator",
                size=13,
                color=DARK_LABEL,
            ),

            ft.Divider(color=DIVIDER_COLOR),

            ft.Text(
                "MAIN FEATURES",
                size=15,
                weight=ft.FontWeight.BOLD,
                color=BURGUNDY,
            ),

            ft.Text("• Student Information Management", size=13, color="#222222",),
            ft.Text("• Tuition Fee Calculation", size=13, color="#222222",),
            ft.Text("• Laboratory Fee Calculation", size=13, color="#222222",),
            ft.Text("• Hands-on Fee Calculation", size=13, color="#222222",),
            ft.Text("• Miscellaneous Fee Breakdown", size=13, color="#222222",),
            ft.Text("• Downpayment and Remaining Balance", size=13, color="#222222",),
            ft.Text("• Saved Enrollment Records", size=13, color="#222222",),
            ft.Text("• Calculation History", size=13, color="#222222",),

            ft.Divider(color=DIVIDER_COLOR),

            ft.Text(
                "DEVELOPED BY",
                size=15,
                weight=ft.FontWeight.BOLD,
                color=BURGUNDY,
            ),

            ft.Container(
                content=ft.Row(
                    controls=[
                        ft.Icon(
                            ft.Icons.PERSON_OUTLINE,
                            color=BURGUNDY,
                            size=24,
                        ),
                        ft.Text(
                            "Aguilar, Mark Jericho M.",
                            size=13,
                            color=DARK_LABEL,
                            weight=ft.FontWeight.W_600,
                        ),
                    ],
                    spacing=10,
                ),
                padding=10,
            ),

            ft.Container(
                content=ft.Row(
                    controls=[
                        ft.Icon(
                            ft.Icons.PERSON_OUTLINE,
                            color=BURGUNDY,
                            size=24,
                        ),
                        ft.Text(
                            "Manzano, Irish Ialle J.",
                            size=13,
                            color=DARK_LABEL,
                            weight=ft.FontWeight.W_600,
                        ),
                    ],
                    spacing=10,
                ),
                padding=10,
            ),

            ft.Container(
                content=ft.Row(
                    controls=[
                        ft.Icon(
                            ft.Icons.PERSON_OUTLINE,
                            color=BURGUNDY,
                            size=24,
                        ),
                        ft.Text(
                            "Mangilit, Joie Louisse M.",
                            size=13,
                            color=DARK_LABEL,
                            weight=ft.FontWeight.W_600,
                        ),
                    ],
                    spacing=10,
                ),
                padding=10,
            ),

            ft.Divider(color=DIVIDER_COLOR),

            ft.Text(
                "BAGUIO COLLEGE OF TECHNOLOGY",
                size=12,
                weight=ft.FontWeight.BOLD,
                color=BURGUNDY,
                text_align=ft.TextAlign.CENTER,
            ),

            ft.Text(
                "Enrollment & Assessment Portal",
                size=11,
                color=MUTED_TEXT,
                text_align=ft.TextAlign.CENTER,
            ),
        ],
        spacing=10,
        scroll=ft.ScrollMode.AUTO,
        expand=True,
    )

    # BACK BUTTON
    back_button = ft.Button(
        "Back to Enrollment",
        icon=ft.Icons.ARROW_BACK,
        bgcolor=BURGUNDY,
        color=WHITE,
        width=float("inf"),
        height=48,
        on_click=lambda e: build_enrollment_page(app),
    )

    # ABOUT CARD
    about_page = ft.Container(
        content=ft.Column(
            controls=[
                about_header,
                ft.Divider(color=DIVIDER_COLOR),
                app_information,
                ft.Container(
                    content=back_button,
                    padding=ft.Padding(0, 10, 0, 0),
                ),
            ],
            spacing=12,
            expand=True,
        ),
        bgcolor=CARD_BACKGROUND,
        border_radius=16,
        padding=24,
        width=460,
        height=740,
        shadow=ft.BoxShadow(
            blur_radius=20,
            color="#1A000000",
            offset=ft.Offset(0, 4),
        ),
    )

    # BACKGROUND
    background_layout = ft.Container(
        image=ft.DecorationImage(
            src="background.png",
            fit=ft.BoxFit.COVER,
        ),
        expand=True,
        width=float("inf"),
        height=float("inf"),
        content=about_page,
        alignment=ft.Alignment(0, 0),
    )

    app.page.add(background_layout)
    app.page.update()


# ==========================================
# HOW TO USE PAGE
# ==========================================

def show_how_to_use(app, e=None):
    app.page.controls.clear()

    # HEADER
    how_to_header = ft.Row(
        controls=[
            ft.IconButton(
                icon=ft.Icons.ARROW_BACK,
                icon_color=BURGUNDY,
                on_click=lambda e: build_enrollment_page(app),
                tooltip="Back to Enrollment",
            ),

            ft.Row(
                controls=[
                    ft.Icon(
                        ft.Icons.HELP_OUTLINE,
                        color=BURGUNDY,
                        size=22,
                    ),

                    ft.Text(
                        "HOW TO USE",
                        size=20,
                        weight=ft.FontWeight.BOLD,
                        color=BURGUNDY,
                    ),
                ],
                spacing=5,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            ),
        ],
        spacing=5,
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
    )

    # INSTRUCTIONS
    instructions = ft.Column(
        controls=[
            ft.Text(
                "1. Student Information",
                size=14,
                weight=ft.FontWeight.BOLD,
                color=BURGUNDY,
            ),

            ft.Text(
                "Enter your Student ID Number and Course / Program.",
                color="#222222",
            ),

            ft.Divider(color=DIVIDER_COLOR),

            ft.Text(
                "2. Personal Information",
                size=14,
                weight=ft.FontWeight.BOLD,
                color=BURGUNDY,
            ),

            ft.Text(
                "Provide your Last Name, First Name, and Middle Initial (M.I.).",
                color="#222222",
            ),

            ft.Divider(color=DIVIDER_COLOR),

            ft.Text(
                "3. Academic Load",
                size=14,
                weight=ft.FontWeight.BOLD,
                color=BURGUNDY,
            ),

            ft.Text(
                "Enter your Total Units, Number of Laboratory classes, "
                "and Number of Hands-on classes.",
                color="#222222",
            ),

            ft.Divider(color=DIVIDER_COLOR),

            ft.Text(
                "4. Downpayment",
                size=14,
                weight=ft.FontWeight.BOLD,
                color=BURGUNDY,
            ),

            ft.Text(
                "Enter the amount of your initial payment.",
                color="#222222",
            ),

            ft.Divider(color=DIVIDER_COLOR),

            ft.Text(
                "5. Calculate Assessment",
                size=14,
                weight=ft.FontWeight.BOLD,
                color=BURGUNDY,
            ),

            ft.Text(
                "Click Calculate Assessment & Submit to calculate "
                "your enrollment fees.",
                color="#222222",
            ),

            ft.Divider(color=DIVIDER_COLOR),

            ft.Text(
                "6. Review Assessment",
                size=14,
                weight=ft.FontWeight.BOLD,
                color=BURGUNDY,
            ),

            ft.Text(
                "Review your calculated fees and assessment details.",
                color="#222222",
            ),

            ft.Divider(color=DIVIDER_COLOR),

            ft.Text(
                "7. Clear Fields",
                size=14,
                weight=ft.FontWeight.BOLD,
                color=BURGUNDY,
            ),

            ft.Text(
                "Click Clear Fields if you want to reset the enrollment form.",
                color="#222222",
            ),
        ],
        spacing=10,
        scroll=ft.ScrollMode.AUTO,
        expand=True,
    )

    # BACK BUTTON
    back_button = ft.Button(
        "Back to Enrollment",
        icon=ft.Icons.ARROW_BACK,
        bgcolor=BURGUNDY,
        color=WHITE,
        width=float("inf"),
        height=48,
        on_click=lambda e: build_enrollment_page(app),
    )

    # HOW TO USE CARD
    how_to_use_page = ft.Container(
        content=ft.Column(
            controls=[
                how_to_header,
                ft.Divider(color=DIVIDER_COLOR),

                ft.Text(
                    "Enrollment & Assessment Guide",
                    size=18,
                    weight=ft.FontWeight.BOLD,
                    color=BURGUNDY,
                ),

                ft.Text(
                    "Follow these steps to use the enrollment calculator.",
                    size=13,
                    color=MUTED_TEXT,
                ),

                ft.Container(height=10),

                instructions,

                ft.Container(
                    content=back_button,
                    padding=ft.Padding(0, 10, 0, 0),
                ),
            ],
            spacing=12,
            expand=True,
        ),
        bgcolor=CARD_BACKGROUND,
        border_radius=16,
        padding=24,
        width=460,
        height=740,
        shadow=ft.BoxShadow(
            blur_radius=20,
            color="#1A000000",
            offset=ft.Offset(0, 4),
        ),
    )

# ==========================================
# EXIT APPLICATION FUNCTION
# ==========================================



    # BACKGROUND
    background_layout = ft.Container(
        image=ft.DecorationImage(
            src="background.png",
            fit=ft.BoxFit.COVER,
        ),
        expand=True,
        width=float("inf"),
        height=float("inf"),
        content=how_to_use_page,
        alignment=ft.Alignment(0, 0),
    )

    app.page.add(background_layout)
    app.page.update()
