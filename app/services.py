from datetime import date
from decimal import Decimal

from sqlalchemy.orm import Session

from app.models import Student


def calculate_pending_amount(
    total_fee: Decimal,
    paid_amount: Decimal,
) -> Decimal:
    pending = total_fee - paid_amount

    if pending < 0:
        return Decimal("0.00")

    return pending


def calculate_fee_status(
    total_fee: Decimal,
    paid_amount: Decimal,
    due_date: date,
) -> str:
    pending_amount = calculate_pending_amount(total_fee, paid_amount)

    if pending_amount == 0:
        return "Paid"

    if due_date < date.today():
        return "Overdue"

    return "Partially Paid"


def get_student_fee(db: Session, student_id: int) -> dict | None:
    student = (
        db.query(Student)
        .filter(Student.StudentID == student_id)
        .first()
    )

    if student is None:
        return None

    pending_amount = calculate_pending_amount(
    student.TotalFee,
    student.PaidAmount,
)

    status = calculate_fee_status(
        student.TotalFee,
        student.PaidAmount,
        student.DueDate,
    )

    return {
        "student_id": student.StudentID,
        "name": student.Name,
        "course": student.Course,
        "email": student.Email,
        "total_fee": student.TotalFee,
        "paid_amount": student.PaidAmount,
        "pending_amount": pending_amount,
        "due_date": student.DueDate,
        "status": status,
    }


def update_student_fee(
    db: Session,
    student_id: int,
    paid_amount: Decimal,
) -> dict | None:

    student = (
        db.query(Student)
        .filter(Student.StudentID == student_id)
        .first()
    )

    if student is None:
        return None

    if paid_amount < 0:
        raise ValueError("Paid amount cannot be negative.")

    if paid_amount > student.TotalFee:
        raise ValueError("Paid amount cannot exceed total fee.")

    student.PaidAmount = paid_amount

    db.commit()
    db.refresh(student)

    pending_amount = calculate_pending_amount(
    student.TotalFee,
    student.PaidAmount,
)
    status = calculate_fee_status(
        student.TotalFee,
        student.PaidAmount,
        student.DueDate,
    )

    return {
        "student_id": student.StudentID,
        "name": student.Name,
        "total_fee": student.TotalFee,
        "paid_amount": student.PaidAmount,
        "pending_amount": pending_amount,
        "due_date": student.DueDate,
        "status": status,
        "updated_at": student.UpdatedAt,
    }

def get_overdue_students(db: Session) -> list[dict]:

    today = date.today()

    students = (
        db.query(Student)
        .filter(
            Student.DueDate < today,
            Student.PaidAmount < Student.TotalFee,
        )
        .order_by(Student.DueDate.asc())
        .all()
    )

    overdue_students = []

    for student in students:
        pending_amount = calculate_pending_amount(
            student.TotalFee,
            student.PaidAmount,
        )

        overdue_students.append({
            "student_id": student.StudentID,
            "name": student.Name,
            "email": student.Email,
            "course": student.Course,
            "total_fee": student.TotalFee,
            "paid_amount": student.PaidAmount,
            "pending_amount": pending_amount,
            "due_date": student.DueDate,
            "status": "Overdue",
        })

    return overdue_students



def get_students(
    db: Session,
    status: str | None = None,
    course: str | None = None,
) -> list[dict]:
    
    students = db.query(Student).all()

    results = []

    for student in students:
        pending_amount = calculate_pending_amount(
            student.TotalFee,
            student.PaidAmount,
        )

        payment_status = calculate_fee_status(
            student.TotalFee,
            student.PaidAmount,
            student.DueDate,
        )

        if status and payment_status.lower() != status.lower():
            continue

        if course and student.Course.lower() != course.lower():
            continue

        results.append({
            "student_id": student.StudentID,
            "name": student.Name,
            "course": student.Course,
            "email": student.Email,
            "total_fee": student.TotalFee,
            "paid_amount": student.PaidAmount,
            "pending_amount": pending_amount,
            "due_date": student.DueDate,
            "status": payment_status,
        })

    return results


def get_fee_summary(db: Session) -> dict:
    """Return fee statistics for administrator dashboard."""

    students = db.query(Student).all()

    total_students = len(students)
    paid_students = 0
    partially_paid_students = 0
    overdue_students = 0

    total_fee = Decimal("0.00")
    total_collected = Decimal("0.00")
    total_pending = Decimal("0.00")

    for student in students:
        pending = calculate_pending_amount(
            student.TotalFee,
            student.PaidAmount,
        )

        status = calculate_fee_status(
            student.TotalFee,
            student.PaidAmount,
            student.DueDate,
        )

        total_fee += student.TotalFee
        total_collected += student.PaidAmount
        total_pending += pending

        if status == "Paid":
            paid_students += 1
        elif status == "Overdue":
            overdue_students += 1
        else:
            partially_paid_students += 1

    return {
        "total_students": total_students,
        "paid_students": paid_students,
        "partially_paid_students": partially_paid_students,
        "overdue_students": overdue_students,
        "total_fee": total_fee,
        "total_collected": total_collected,
        "total_pending": total_pending,
    }