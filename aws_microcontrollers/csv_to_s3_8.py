
from services.aws.s3_service import upload_file_to_s3_bucket


def upload_to_s3(s3_client, file_path, bucket_name, key):
    upload_file_to_s3_bucket(
        s3_client=s3_client,
        file_path=file_path,
        bucket_name=bucket_name,
        key=key
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
    upload_to_s3(
        s3_client=s3_test_client,
        file_path=settings.INITIAL_DB_DATA_PATH,
        bucket_name=settings.AWS_BUCKET_NAMES.get('csv'),
        key=settings.FILE_NAME_IN_BUCKET
    )
