from os import listdir

import settings
import generic_services
from aws_s3_bucket_services import upload_file_to_s3_bucket


def upload_zips_to_s3(s3_client,
                      directory_path_lambda,
                      directory_path_zip_storage):
    for file_name in listdir(directory_path_lambda):
        zip_file_name = generic_services.get_zip_file_name(file_name)
        zip_file_path = generic_services.get_zip_file_path(
            directory_path_zip_storage=directory_path_zip_storage,
            file_name=file_name
        )
        upload_file_to_s3_bucket(
            s3_client=s3_client,
            file_path=zip_file_path,
            bucket_name=settings.AWS_BUCKET_NAME_LAMBDA,
            key=zip_file_name
        )


if __name__ == '__main__':
    from aws_boto3_client import Boto3Client
    boto_client = Boto3Client(
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY
    )
    s3_test_client = boto_client.get_s3_client()
    upload_zips_to_s3(
        s3_client=s3_test_client,
        directory_path_lambda=settings.DIRECTORY_PATH_LAMBDA,
        directory_path_zip_storage=settings.DIRECTORY_PATH_ZIP_STORAGE
    )
