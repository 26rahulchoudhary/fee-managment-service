import json
from decimal import Decimal, InvalidOperation

import azure.functions as func

from app.database import SessionLocal
from app.services import update_student_fee


def admin_fee_update(req: func.HttpRequest) -> func.HttpResponse:
    student_id = req.route_params.get("student_id")

    if not student_id:
        return func.HttpResponse(
            json.dumps({"error": "Student ID is required"}),
            status_code=400,
            mimetype="application/json",
        )

    try:
        student_id = int(student_id)
    except ValueError:
        return func.HttpResponse(
            json.dumps({"error": "Student ID must be an integer"}),
            status_code=400,
            mimetype="application/json",
        )

    try:
        body = req.get_json()
        paid_amount = Decimal(str(body.get("paid_amount")))
    except (ValueError, TypeError, InvalidOperation):
        return func.HttpResponse(
            json.dumps({"error": "paid_amount must be a valid number"}),
            status_code=400,
            mimetype="application/json",
        )

    db = SessionLocal()

    try:
        result = update_student_fee(
            db,
            student_id,
            paid_amount,
        )

        if result is None:
            return func.HttpResponse(
                json.dumps({"error": "Student not found"}),
                status_code=404,
                mimetype="application/json",
            )

        return func.HttpResponse(
            json.dumps(result, default=str),
            status_code=200,
            mimetype="application/json",
        )

    except ValueError as error:
        db.rollback()

        return func.HttpResponse(
            json.dumps({"error": str(error)}),
            status_code=400,
            mimetype="application/json",
        )

    except Exception as error:
        db.rollback()
        print(f"Error updating student fee: {error}")

        return func.HttpResponse(
            json.dumps({"error": "Internal server error"}),
            status_code=500,
            mimetype="application/json",
        )

    finally:
        db.close()