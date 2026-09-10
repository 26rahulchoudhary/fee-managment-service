from datetime import date, datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


class StudentFeeResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    student_id: int
    name: str
    course: str
    email: str

    total_fee: Decimal
    paid_amount: Decimal
    pending_amount: Decimal

    due_date: date
    status: str


class FeeUpdateRequest(BaseModel):
    paid_amount: Decimal = Field(ge=0)


class FeeUpdateResponse(BaseModel):
    student_id: int
    name: str
    total_fee: Decimal
    paid_amount: Decimal
    pending_amount: Decimal

    due_date: date
    status: str
    updated_at: datetime | None = None