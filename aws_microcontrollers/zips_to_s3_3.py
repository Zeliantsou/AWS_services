
from os import listdir

from services.generic.generic_services import (
    get_zip_file_name,
    get_zip_file_path
)
from services.aws.s3_service import upload_file_to_s3_bucket


def upload_zips_to_s3(s3_client,
                      directory_path_lambda,
                      directory_path_zip_storage,
                      bucket_name):
    for file_name in listdir(directory_path_lambda):
        zip_file_name = get_zip_file_name(file_name)
        zip_file_path = get_zip_file_path(
            directory_path_zip_storage=directory_path_zip_storage,
            file_name=file_name
        )
        upload_file_to_s3_bucket(
            s3_client=s3_client,
            file_path=zip_file_path,
            bucket_name=bucket_name,
            key=zip_file_name
        )


if __name__ == '__main__':
    import sys
    import os
    import settings
    from services.aws.boto3_client_service import Boto3Client

    dir_name = os.path.dirname(os.path.abspath(__file__))
    sys.path.append(os.path.dirname(dir_name))

    boto_client = Boto3Client(
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY
    )
    s3_test_client = boto_client.get_s3_client()
    upload_zips_to_s3(
        s3_client=s3_test_client,
        directory_path_lambda=settings.DIRECTORY_PATH_LAMBDA,
        directory_path_zip_storage=settings.DIRECTORY_PATH_ZIP_STORAGE,
        bucket_name=settings.AWS_BUCKET_NAMES.get('lambda')
    )
