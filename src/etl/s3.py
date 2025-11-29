"""Helper functions for interacting with AWS S3."""

import boto3
from botocore.exceptions import BotoCoreError, NoCredentialsError
from core.config import settings
from core.logger import get_logger
from core.utils import ensure_dir
from pathlib import Path

logger = get_logger()


def get_s3_client() -> boto3.client:
    """Create and return a boto3 S3 client using configured credentials."""
    if not settings.aws_access_key_id or not settings.aws_secret_access_key:
        raise RuntimeError("AWS credentials are not configured. Please set aws_access_key_id and aws_secret_access_key in your .env file.")

    return boto3.client(
        "s3",
        aws_access_key_id=settings.aws_access_key_id,
        aws_secret_access_key=settings.aws_secret_access_key,
        aws_session_token=settings.aws_session_token,
        region_name=settings.aws_region,
    )


def download_from_s3(key: str, destination_dir: str | None = None) -> str:
    """Download a file from S3 to the local filesystem.

    Args:
        key: The key of the S3 object to download.
        destination_dir: Local directory where the file should be saved. If None, uses settings.raw_dir.

    Returns:
        Path to the downloaded file.
    """
    bucket = settings.s3_bucket
    if not bucket:
        raise RuntimeError("S3 bucket name is not configured. Set s3_bucket in your .env file.")

    dest_dir = destination_dir or settings.raw_dir
    ensure_dir(dest_dir)
    filename = Path(key).name
    dest_path = str(Path(dest_dir) / filename)

    client = get_s3_client()
    try:
        logger.info(f"Downloading s3://{bucket}/{key} to {dest_path}")
        client.download_file(bucket, key, dest_path)
    except (BotoCoreError, NoCredentialsError) as e:
        raise RuntimeError(f"Failed to download {key} from S3: {e}")

    return dest_path