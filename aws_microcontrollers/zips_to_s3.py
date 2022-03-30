
from os import listdir
import logging

from botocore.exceptions import ClientError

from services.generic.generic_services import (
    get_zip_file_name,
    get_zip_file_path
)
from services.aws.s3_service import upload_file_to_s3_bucket


logger = logging.getLogger(__name__)


def upload_zips_to_s3(
        s3_client,
        directory_path_lambda: str,
        directory_path_zip_storage: str,
        bucket_name: str
) -> None:
    """
    Uploads zip files to the S3 bucket for lambda functions.
    """
    for file_name in listdir(directory_path_lambda):
        try:
            zip_file_name = get_zip_file_name(file_name)
            zip_file_path = get_zip_file_path(
                directory_path_zip_storage=directory_path_zip_storage,
                file_name=file_name
            )
        except Exception:
            logger.exception(
                f'Could not get zip file path or zip file name')
            raise
        try:
            upload_file_to_s3_bucket(
                s3_client=s3_client,
                file_path=zip_file_path,
                bucket_name=bucket_name,
                key=zip_file_name
            )
        except ClientError:
            logger.exception(
                (f'Could not upload file with {zip_file_name}'
                 f'to the bucket "{bucket_name}"')
            )
            raise
