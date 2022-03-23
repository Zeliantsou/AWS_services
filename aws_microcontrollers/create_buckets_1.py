import settings
from aws_s3_bucket_services import create_s3_bucket


def create_buckets(s3_client):

    create_s3_bucket(
        s3_client=s3_client,
        bucket_name=settings.AWS_BUCKET_NAME_CSV,
        region=settings.AWS_DEFAULT_REGION
    )
    create_s3_bucket(
        s3_client=s3_client,
        bucket_name=settings.AWS_BUCKET_NAME_LAMBDA,
        region=settings.AWS_DEFAULT_REGION
    )


if __name__ == '__main__':
    from aws_boto3_client import Boto3Client
    boto_client = Boto3Client(
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY
    )
    s3_test_client = boto_client.get_s3_client()
    create_buckets(s3_client=s3_test_client)
