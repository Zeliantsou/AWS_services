import settings

from aws_iam_services import get_iam_role_arn
from aws_s3_bucket_services import get_list_objects, get_key_objects
from aws_lambda_services import (
    create_lambda_function,
    get_lambda_function_name,
    get_lambda_handler
)


def create_lambda_functions(iam_client, s3_client, lambda_client):
    role_arn = get_iam_role_arn(
        iam_client=iam_client,
        role_name=settings.AWS_ROLE_NAME  # 'cereal-csv-2dynamoDB'
    )
    bucket_objects = get_list_objects(
        s3_client=s3_client,
        bucket_name=settings.AWS_BUCKET_NAME_LAMBDA
    )
    keys = get_key_objects(bucket_objects)
    for key in keys:
        code_data = {
            'S3Bucket': settings.AWS_BUCKET_NAME_LAMBDA,
            'S3Key': key,
        }
        create_lambda_function(
            lambda_client=lambda_client,
            code_data=code_data,
            function_name=get_lambda_function_name(key),
            role_arn=role_arn,
            handler=get_lambda_handler(key)
        )


if __name__ == '__main__':
    from aws_boto3_client import Boto3Client
    boto3_client = Boto3Client(
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY
    )
    iam_test_client = boto3_client.get_iam_client()
    s3_test_client = boto3_client.get_s3_client()
    lambda_test_client = boto3_client.get_lambda_client()
    create_lambda_functions(
        iam_client=iam_test_client,
        s3_client=s3_test_client,
        lambda_client=lambda_test_client
    )
