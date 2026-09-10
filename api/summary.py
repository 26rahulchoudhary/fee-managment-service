import json

import azure.functions as func

from app.database import SessionLocal
from app.services import get_fee_summary


def fee_summary(req: func.HttpRequest) -> func.HttpResponse:
    db = SessionLocal()

    try:
        summary = get_fee_summary(db)

        return func.HttpResponse(
            json.dumps(summary, default=str),
            status_code=200,
            mimetype="application/json",
        )

    except Exception as error:
        print(f"Error generating summary: {error}")

        return func.HttpResponse(
            json.dumps({"error": "Internal server error"}),
            status_code=500,
            mimetype="application/json",
        )

    finally:
        db.close()