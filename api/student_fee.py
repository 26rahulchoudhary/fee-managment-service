import azure.functions as func
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.services import get_student_fee


def student_fee(req: func.HttpRequest) -> func.HttpResponse:
    student_id = req.route_params.get("student_id")

    if not student_id:
        return func.HttpResponse(
            '{"error": "Student ID is required"}',
            status_code=400,
            mimetype="application/json",
        )

    try:
        student_id = int(student_id)
    except ValueError:
        return func.HttpResponse(
            '{"error": "Student ID must be an integer"}',
            status_code=400,
            mimetype="application/json",
        )

    db: Session = SessionLocal()

    try:
        result = get_student_fee(db, student_id)

        if result is None:
            return func.HttpResponse(
                '{"error": "Student not found"}',
                status_code=404,
                mimetype="application/json",
            )

        import json

        return func.HttpResponse(
            json.dumps(result, default=str),
            status_code=200,
            mimetype="application/json",
        )

    except Exception as error:
        print(f"Error fetching student fee: {error}")

        return func.HttpResponse(
            '{"error": "Internal server error"}',
            status_code=500,
            mimetype="application/json",
        )

    finally:
        db.close()