from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    """Application settings loaded from environment variables or a `.env` file.

    The `.env` file can be created from `.env.example` and should contain your secrets.
    """

    # General
    app_name: str = Field("Enterprise Data Platform", description="Name of the application")
    environment: str = Field("dev", description="Application environment (dev/staging/prod)")

    # Logging
    log_level: str = Field("INFO", description="Logging level")

    # Data directories
    data_dir: str = Field("data", description="Base directory for data")
    raw_dir: str = Field("data/raw", description="Directory for raw input files")
    processed_dir: str = Field("data/processed", description="Directory for processed files")
    cache_dir: str = Field("data/cache", description="Directory for cached files")

    # AWS S3 configuration
    aws_access_key_id: str | None = Field(default=None, description="AWS access key ID")
    aws_secret_access_key: str | None = Field(default=None, description="AWS secret access key")
    aws_session_token: str | None = Field(default=None, description="AWS session token if using STS")
    aws_region: str | None = Field(default=None, description="AWS region")
    s3_bucket: str | None = Field(default=None, description="Default S3 bucket name")

    # Snowflake configuration
    snowflake_account: str | None = Field(default=None, description="Snowflake account identifier")
    snowflake_user: str | None = Field(default=None, description="Snowflake username")
    snowflake_password: str | None = Field(default=None, description="Snowflake password")
    snowflake_role: str | None = Field(default=None, description="Snowflake role")
    snowflake_warehouse: str | None = Field(default=None, description="Snowflake warehouse")
    snowflake_database: str | None = Field(default=None, description="Snowflake database")
    snowflake_schema: str | None = Field(default=None, description="Snowflake schema")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()