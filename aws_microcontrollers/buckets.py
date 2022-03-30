
import logging

from botocore.exceptions import ClientError

from services.aws.s3_service import (
    create_s3_bucket,
    create_all_s3_buckets
)


logger = logging.getLogger(__name__)


@create_all_s3_buckets
def create_buckets(
        s3_client,
        bucket_name: str,
        region: str
) -> None:
    """
    Creates all buckets that necessary for project.
    """
    try:
        create_s3_bucket(
            s3_client=s3_client,
            bucket_name=bucket_name,
            region=region
        )
    except ClientError:
        logger.exception(
            f'Could not create a bucket with name "{bucket_name}"')
        raise
