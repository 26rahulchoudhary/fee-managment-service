import json

import azure.functions as func

from app.database import SessionLocal
from app.services import get_students


def students_list(req: func.HttpRequest) -> func.HttpResponse:
    status = req.params.get("status")
    course = req.params.get("course")

    db = SessionLocal()

    try:
        students = get_students(
            db=db,
            status=status,
            course=course,
        )

        return func.HttpResponse(
            json.dumps(students, default=str),
            status_code=200,
            mimetype="application/json",
        )

    except Exception as error:
        print(f"Error fetching students: {error}")

        return func.HttpResponse(
            json.dumps({"error": "Internal server error"}),
            status_code=500,
            mimetype="application/json",
        )

    finally:
        db.close()