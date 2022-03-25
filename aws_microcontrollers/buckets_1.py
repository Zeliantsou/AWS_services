
from services.aws.s3_service import (
    create_s3_bucket,
    create_all_s3_buckets
)


@create_all_s3_buckets
def create_buckets(s3_client, bucket_name, region):
    create_s3_bucket(
        s3_client=s3_client,
        bucket_name=bucket_name,
        region=region
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
    create_buckets(
        dict_bucket_names=settings.AWS_BUCKET_NAMES,
        s3_client=s3_test_client,
        region=settings.AWS_DEFAULT_REGION,
    )
