import uuid

import settings
from aws_lambda_services import (
    add_permission_for_lambda,
    get_policy_for_lambda,
    create_destination_for_lambda
)
from aws_s3_bucket_services import create_bucket_notification_configuration


def create_triggers_and_destinations(lambda_client, s3_client):

    function_arn = (f'arn:aws:lambda:{settings.AWS_DEFAULT_REGION}:'
                    f'{settings.AWS_ACCOUNT_ID}:'
                    f'function:delete_existing_table')

    source_arn = f'arn:aws:s3:::{settings.AWS_BUCKET_NAME_CSV}'

    add_permission_for_lambda(
        lambda_client=lambda_client,
        action='lambda:InvokeFunction',
        function_name=function_arn,
        principal='s3.amazonaws.com',
        source_arn=source_arn,
        statement_id=uuid.uuid4().hex
    )
    get_policy_for_lambda(
        lambda_client=lambda_client,
        function_arn=function_arn
    )
    create_bucket_notification_configuration(
        s3_client=s3_client,
        bucket_name=settings.AWS_BUCKET_NAME_CSV,
        function_arn=function_arn,
        events=['s3:ObjectCreated:Put']
    )
    destin_arn_for_del_exist_table = (
        f'arn:aws:lambda:{settings.AWS_DEFAULT_REGION}:'
        f'{settings.AWS_ACCOUNT_ID}:'
        f'function:create_new_table'
    )
    destin_arn_for_create_new_table = (
        f'arn:aws:lambda:{settings.AWS_DEFAULT_REGION}:'
        f'{settings.AWS_ACCOUNT_ID}:'
        f'function:fill_new_table'
    )
    create_destination_for_lambda(
        lambda_client=lambda_client,
        function_name='delete_existing_table',
        destination_arn=destin_arn_for_del_exist_table
    )
    create_destination_for_lambda(
        lambda_client=lambda_client,
        function_name='create_new_table',
        destination_arn=destin_arn_for_create_new_table
    )


if __name__ == '__main__':
    from aws_boto3_client import Boto3Client
    boto3_client = Boto3Client(
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY
    )
    lambda_test_client = boto3_client.get_lambda_client()
    s3_test_client = boto3_client.get_s3_client()

    create_triggers_and_destinations(
        lambda_client=lambda_test_client,
        s3_client=s3_test_client
    )
