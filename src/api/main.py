"""FastAPI application entry point."""

from fastapi import FastAPI

from .routers.validate import router as validate_router

app = FastAPI(
    title="Enterprise Data Platform API",
    description="API for data validation and operations",
    version="1.0.0",
)

# Include routers
app.include_router(validate_router)


@app.get("/health")
def health() -> dict[str, str]:
    """Health check endpoint."""
    return {"status": "ok"}
