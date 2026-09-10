import azure.functions as func
from api.student_fee import student_fee as student_fee_api
from api.admin_fee import admin_fee_update 

app = func.FunctionApp(http_auth_level=func.AuthLevel.FUNCTION)


@app.route(route="health", methods=["GET"])
def health(req: func.HttpRequest) -> func.HttpResponse:
    return func.HttpResponse(
        body="""
        {
            "status": "healthy",
            "service": "Fee Management System",
            "version": "1.0.0"
        }
        """,
        status_code=200,
        mimetype="application/json",
    )


@app.route(
    route="student/{student_id}/fee",
    methods=["GET"],
    auth_level=func.AuthLevel.FUNCTION,
)
def student_fee(req: func.HttpRequest) -> func.HttpResponse:
    return student_fee_api(req)



@app.route(
    route="fee/admin/student/{student_id}",
    methods=["PUT"],
    auth_level=func.AuthLevel.FUNCTION,
)
def update_admin_fee(req: func.HttpRequest) -> func.HttpResponse:
    return admin_fee_update(req)