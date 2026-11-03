
import flet as ft
from config import BURGUNDY, CARD_BACKGROUND, DIVIDER_COLOR
from datetime import datetime

PER_UNIT_RATE = 459.54
LAB_FEE = 3429.30
HANDS_ON_FEE = 2341.86
DOWNPAYMENT = 3500.00

MISC_FEES = [
    ("Registration", 621.00),
    ("Library", 552.00),
    ("Athletic", 445.74),
    ("ID Card", 414.00),
    ("SBO", 124.20),
    ("Publication", 124.20),
    ("Insurance", 31.74),
    ("Health Services", 231.38),
    ("Socio Cultural", 165.60),
    ("Guidance & Counseling", 124.20),
    ("Audio Visual", 154.56),
    ("Faculty Development Fund", 386.40),
    ("Infrastructure", 154.56),
    ("Internet", 110.40),
    ("Prisaa", 100.00),
]


def money(value):
    return f"{value:,.2f}"


def quantity_row(label, value):
    return ft.Row(
        controls=[
            ft.Text(
                label,
                size=12,
                color="#222222",
                expand=True,
            ),
            ft.Text(
                str(value),
                size=12,
                color="#222222",
            ),
        ],
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        vertical_alignment=ft.CrossAxisAlignment.START,
    )


def show_results(app, data):
    page = app.page

    # RESPONSIVE CARD DIMENSIONS
    screen_width = page.width or 360

    card_width = min(
        460,
        max(280, screen_width - 24)
    )

    card_padding = 16 if screen_width < 400 else 24
    button_width = card_width - (card_padding * 2)

    # SAVE ENROLLMENT INPUTS
    app.saved_inputs = {
        "student_id": str(data.get("student_id") or ""),
        "course": str(data.get("course") or ""),
        "last_name": str(data.get("last_name") or ""),
        "first_name": str(data.get("first_name") or ""),
        "mi": str(
            data.get("middle_initial", data.get("mi", "")) or ""
        ),
        "total_units": str(
            data.get("units", data.get("total_units", ""))
        ),
        "lab_classes": str(
            data.get("laboratory", data.get("lab_classes", ""))
        ),
        "hands_on": str(
            data.get("hands_on", data.get("hands-on", ""))
        ),
        "downpayment": str(
            data.get("down_payment", data.get("downpayment", ""))
        ),
    }

    first_name = app.saved_inputs["first_name"]
    middle_initial = app.saved_inputs["mi"]
    last_name = app.saved_inputs["last_name"]

    full_name = " ".join(
        part for part in (first_name, middle_initial, last_name)
        if part
    )

    def get_nonnegative_int(*keys):
        for key in keys:
            value = data.get(key)

            if value is not None and str(value).strip() != "":
                try:
                    return max(0, int(value))
                except (TypeError, ValueError):
                    return 0

        return 0

    units = get_nonnegative_int("units", "total_units")
    laboratory = get_nonnegative_int("laboratory", "lab_classes")
    hands_on = get_nonnegative_int("hands_on", "hands-on")

    # ASSESSMENT COMPUTATION
    units_tuition = PER_UNIT_RATE * units
    laboratory_tuition = LAB_FEE * laboratory
    handson_tuition = HANDS_ON_FEE * hands_on

    miscellaneous_total = sum(
        amount for _, amount in MISC_FEES
    )

    total_assessment = (
        units_tuition
        + laboratory_tuition
        + handson_tuition
        + miscellaneous_total
    )

    downpayment_value = data.get(
        "down_payment",
        data.get("downpayment", DOWNPAYMENT),
    )

    try:
        downpayment = max(
            0.0,
            float(downpayment_value or 0)
        )
    except (TypeError, ValueError):
        downpayment = DOWNPAYMENT

    balance_after_downpayment = max(
        0,
        total_assessment - downpayment,
    )

    # EXAM COMPUTATION
    # All percentages are based on the remaining balance.

    exam_base = balance_after_downpayment

    first_prelim = round(exam_base * 0.15, 2)
    first_grading = round(exam_base * 0.25, 2)
    second_prelim = round(exam_base * 0.15, 2)
    midterm = round(exam_base * 0.30, 2)
    finals = round(exam_base * 0.15, 2)

    total_exam_computation = (
        first_prelim
        + first_grading
        + second_prelim
        + midterm
        + finals
    )

    # SAVE ENROLLMENT RECORD
    record = {
        "student_id": app.saved_inputs["student_id"],
        "course": app.saved_inputs["course"],
        "first_name": first_name,
        "middle_initial": middle_initial,
        "last_name": last_name,
        "full_name": full_name,
        "total_units": units,
        "laboratory": laboratory,
        "hands_on": hands_on,
        "units_tuition": units_tuition,
        "laboratory_tuition": laboratory_tuition,
        "handson_tuition": handson_tuition,
        "miscellaneous_fees": MISC_FEES.copy(),
        "miscellaneous_total": miscellaneous_total,
        "total_assessment": total_assessment,
        "downpayment": downpayment,
        "remaining_balance": balance_after_downpayment,

        # EXAM COMPUTATION VALUES
        "first_prelim": first_prelim,
        "first_grading": first_grading,
        "second_prelim": second_prelim,
        "midterm": midterm,
        "finals": finals,
        "exam_computation": total_exam_computation,

        "date": datetime.now().strftime("%Y-%m-%d %I:%M %p"),
    }

    app.records.append(record)

    app.calculation_history.append({
        "student_id": record["student_id"],
        "full_name": record["full_name"],
        "total_assessment": total_assessment,
        "date": record["date"],
    })

    # FEE ROW
    def fee_row(label, amount, bold=False):
        return ft.Row(
            controls=[
                ft.Text(
                    label,
                    size=12,
                    color="#222222",
                    expand=True,
                    weight=(
                        ft.FontWeight.BOLD
                        if bold
                        else ft.FontWeight.NORMAL
                    ),
                ),
                ft.Text(
                    f"₱{money(amount)}",
                    size=12,
                    color="#222222",
                    weight=(
                        ft.FontWeight.BOLD
                        if bold
                        else ft.FontWeight.NORMAL
                    ),
                ),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.START,
        )

    # STUDENT INFORMATION
    student_info = ft.Column(
        controls=[
            ft.Text(
                "STUDENT INFORMATION",
                size=14,
                weight=ft.FontWeight.BOLD,
                color=BURGUNDY,
            ),
            ft.Divider(color=DIVIDER_COLOR),

            ft.Row(
                controls=[
                    ft.Text(
                        "Student ID",
                        size=12,
                        color="#222222",
                        expand=True,
                    ),
                    ft.Text(
                        app.saved_inputs["student_id"] or "N/A",
                        size=12,
                        color="#222222",
                        weight=ft.FontWeight.BOLD,
                        text_align=ft.TextAlign.RIGHT,
                    ),
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            ),

            ft.Row(
                controls=[
                    ft.Text(
                        "Full Name",
                        size=12,
                        color="#222222",
                        expand=True,
                    ),
                    ft.Text(
                        full_name or "N/A",
                        size=12,
                        color="#222222",
                        weight=ft.FontWeight.BOLD,
                        text_align=ft.TextAlign.RIGHT,
                    ),
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            ),

            ft.Row(
                controls=[
                    ft.Text(
                        "Course",
                        size=12,
                        color="#222222",
                        expand=True,
                    ),
                    ft.Text(
                        app.saved_inputs["course"] or "N/A",
                        size=12,
                        color="#222222",
                        weight=ft.FontWeight.BOLD,
                        text_align=ft.TextAlign.RIGHT,
                    ),
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            ),

            quantity_row("Total Units", units),
            quantity_row("No. of Laboratory", laboratory),
            quantity_row("No. of Hands-on", hands_on),
        ],
        spacing=8,
    )

    # ASSESSMENT BREAKDOWN
    assessment_breakdown = ft.Column(
        controls=[
            ft.Text(
                "ASSESSMENT BREAKDOWN",
                size=14,
                weight=ft.FontWeight.BOLD,
                color=BURGUNDY,
            ),
            ft.Divider(color=DIVIDER_COLOR),

            fee_row(
                f"Tuition ({units} units × ₱{money(PER_UNIT_RATE)})",
                units_tuition,
            ),

            fee_row(
                f"Laboratory Fee ({laboratory} × ₱{money(LAB_FEE)})",
                laboratory_tuition,
            ),

            fee_row(
                f"Hands-on Fee ({hands_on} × ₱{money(HANDS_ON_FEE)})",
                handson_tuition,
            ),

            ft.Container(height=4),

            ft.Text(
                "MISCELLANEOUS FEES",
                size=12,
                weight=ft.FontWeight.BOLD,
                color=BURGUNDY,
            ),

            *[
                fee_row(label, amount)
                for label, amount in MISC_FEES
            ],

            ft.Divider(color=DIVIDER_COLOR),

            fee_row(
                "Total Miscellaneous Fees",
                miscellaneous_total,
                bold=True,
            ),

            ft.Divider(color=DIVIDER_COLOR),

            fee_row(
                "TOTAL ASSESSMENT",
                total_assessment,
                bold=True,
            ),
        ],
        spacing=7,
    )

    # PAYMENT SUMMARY
    payment_summary = ft.Column(
        controls=[
            ft.Text(
                "PAYMENT SUMMARY",
                size=14,
                weight=ft.FontWeight.BOLD,
                color=BURGUNDY,
            ),
            ft.Divider(color=DIVIDER_COLOR),

            # EXAM COMPUTATION
            ft.Text(
                "EXAM COMPUTATION",
                size=12,
                weight=ft.FontWeight.BOLD,
                color=BURGUNDY,
            ),

            fee_row(
                "1st Prelim (15%)",
                first_prelim,
            ),

            fee_row(
                "1st Grading (25%)",
                first_grading,
            ),

            fee_row(
                "2nd Prelim (15%)",
                second_prelim,
            ),

            fee_row(
                "Midterm (30%)",
                midterm,
            ),

            fee_row(
                "Finals (15%)",
                finals,
            ),

            ft.Divider(color=DIVIDER_COLOR),

            # PAYMENT DETAILS
            fee_row(
                "Downpayment",
                downpayment,
                bold=True,
            ),

            fee_row(
                "Remaining Balance",
                balance_after_downpayment,
                bold=True,
            ),
        ],
        spacing=8,
    )

    # COMPUTATION GUIDE
    explanation = ft.Column(
        controls=[
            ft.Text(
                "COMPUTATION GUIDE",
                size=14,
                weight=ft.FontWeight.BOLD,
                color=BURGUNDY,
            ),
            ft.Divider(color=DIVIDER_COLOR),

            ft.Text(
                "• Tuition is computed by multiplying the "
                "per-unit rate by the total number of units.",
                size=11,
                color="#222222",
            ),

            ft.Text(
                "• Laboratory and hands-on fees are multiplied "
                "by their respective quantities.",
                size=11,
                color="#222222",
            ),

            ft.Text(
                "• Miscellaneous fees are added to tuition "
                "and other fees.",
                size=11,
                color="#222222",
            ),

            ft.Text(
                f"• Remaining balance is the total assessment "
                f"less the ₱{money(downpayment)} downpayment.",
                size=11,
                color="#222222",
            ),

            ft.Text(
                "• Exam computation is divided into five "
                "payments based on the remaining balance:",
                size=11,
                color="#222222",
            ),

            ft.Text(
                "  - 1st Prelim: 15%",
                size=11,
                color="#222222",
            ),

            ft.Text(
                "  - 1st Grading: 25%",
                size=11,
                color="#222222",
            ),

            ft.Text(
                "  - 2nd Prelim: 15%",
                size=11,
                color="#222222",
            ),

            ft.Text(
                "  - Midterm: 30%",
                size=11,
                color="#222222",
            ),

            ft.Text(
                "  - Finals: 15%",
                size=11,
                color="#222222",
            ),
        ],
        spacing=7,
    )

    # BACK TO ENROLLMENT
    def back_to_enrollment(e):
        saved = app.saved_inputs.copy()

        page.controls.clear()
        app.build_ui()

        # RESTORE SAVED VALUES
        app.student_id.value = saved["student_id"]
        app.course.value = saved["course"]
        app.last_name.value = saved["last_name"]
        app.first_name.value = saved["first_name"]
        app.mi.value = saved["mi"]
        app.total_units.value = saved["total_units"]
        app.lab_classes.value = saved["lab_classes"]
        app.hands_on.value = saved["hands_on"]
        app.downpayment.value = saved["downpayment"]

        page.update()

    # RESULT CONTENT
    result_content = ft.Column(
    controls=[
        ft.Text(
            "ASSESSMENT SUMMARY",
            size=20,
            weight=ft.FontWeight.BOLD,
            color=BURGUNDY,
            text_align=ft.TextAlign.CENTER,
        ),

        ft.Divider(color=DIVIDER_COLOR),

        student_info,

        ft.Container(height=8),

        assessment_breakdown,

        ft.Container(height=8),

        # Exam Computation is already inside Payment Summary
        payment_summary,

        ft.Container(height=8),

        explanation,

        ft.Container(height=12),

        ft.Button(
            content="Back to Enrollment",
            width=button_width,
            bgcolor=BURGUNDY,
            color="#FFFFFF",
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=8),
            ),
            on_click=back_to_enrollment,
        ),
    ],
    spacing=10,
    scroll=ft.ScrollMode.AUTO,
    expand=True,
)

    # RESULT CARD
    result_card = ft.Container(
        content=result_content,
        width=card_width,
        height=600,
        padding=card_padding,
        bgcolor=CARD_BACKGROUND,
        border_radius=16,
        shadow=ft.BoxShadow(
            spread_radius=1,
            blur_radius=15,
            color="#20000000",
            offset=ft.Offset(0, 5),
        ),
    )

    # BACKGROUND
    background = ft.Container(
        content=ft.Row(
            controls=[result_card],
            alignment=ft.MainAxisAlignment.CENTER,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        expand=True,
        image=ft.DecorationImage(
            src="background.png",
            fit=ft.BoxFit.COVER,
        ),
        alignment=ft.Alignment(0, 0),
    )

    page.controls.clear()
    page.add(background)
    page.update()
