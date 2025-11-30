"""API models used by FastAPI endpoints."""

from pydantic import BaseModel, EmailStr, Field


class Record(BaseModel):
    """Schema representing a simple record with id, email and age."""

    id: int = Field(..., gt=0)
    email: EmailStr
    age: int = Field(..., gt=0, lt=120)
