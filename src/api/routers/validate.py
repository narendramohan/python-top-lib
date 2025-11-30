"""API router providing a CSV validation endpoint."""

import polars as pl
from fastapi import APIRouter, UploadFile

from ...core.logger import get_logger
from ..models import Record

router = APIRouter(prefix="/validate", tags=["validate"])
logger = get_logger()


@router.post("/")
async def validate(file: UploadFile):
    """Validate uploaded CSV records against the Record schema.

    Reads the uploaded file into a Polars DataFrame and validates each row according to the Record model.
    Returns the number of rows and any errors encountered.
    """
    df = pl.read_csv(file.file)  # Directly read from the uploaded file-like object
    errors: list[dict] = []
    for row in df.to_dicts():
        try:
            Record(**row)
        except Exception as e:
            errors.append({"row": row, "error": str(e)})

    result = {"rows": len(df), "errors": errors}
    logger.info(f"Validated {result['rows']} rows with {len(errors)} errors")
    return result
