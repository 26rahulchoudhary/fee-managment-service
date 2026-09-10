from datetime import date
from decimal import Decimal

from sqlalchemy.orm import Session

from app.models import Student


def calculate_fee_status(
    total_fee: Decimal,
    paid_amount: Decimal,
    due_date: date,
) -> tuple[Decimal, str]:
    pending_amount = total_fee - paid_amount

    if pending_amount <= 0:
        return Decimal("0.00"), "Paid"

    if due_date < date.today():
        return pending_amount, "Overdue"

    return pending_amount, "Partially Paid"


def get_student_fee(db: Session, student_id: int) -> dict | None:
    student = (
        db.query(Student)
        .filter(Student.StudentID == student_id)
        .first()
    )

    if student is None:
        return None

    pending_amount, status = calculate_fee_status(
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

    pending_amount, status = calculate_fee_status(
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