
import logging

from botocore.exceptions import ClientError

from services.aws.s3_service import upload_file_to_s3_bucket


logger = logging.getLogger(__name__)


def upload_to_s3(
        s3_client,
        file_path: str,
        bucket_name: str,
        key: str):
    """
    Uploads file to the S3 bucket.
    """
    try:
        upload_file_to_s3_bucket(
            s3_client=s3_client,
            file_path=file_path,
            bucket_name=bucket_name,
            key=key
        )
    except ClientError:
        logger.exception(
            (f'Could not upload "{key}" file'
             f'to the "{bucket_name}" bucket')
        )
        raise
