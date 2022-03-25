
import uuid

from services.aws.lambda_service import (
    add_permission_for_lambda,
    get_policy_for_lambda,
    create_destination_for_lambda
)
from services.aws.s3_service import (
    create_bucket_notification_configuration)


def create_triggers_and_destinations(lambda_client, s3_client,
                                     region, aws_account_id,
                                     bucket_name):

    function_arn = (f'arn:aws:lambda:{region}:'
                    f'{aws_account_id}:'
                    f'function:delete_existing_table')

    source_arn = f'arn:aws:s3:::{bucket_name}'

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
        bucket_name=bucket_name,
        function_arn=function_arn,
        events=['s3:ObjectCreated:Put']
    )
    destin_arn_for_del_exist_table = (
        f'arn:aws:lambda:{region}:'
        f'{aws_account_id}:'
        f'function:create_new_table'
    )
    destin_arn_for_create_new_table = (
        f'arn:aws:lambda:{region}:'
        f'{aws_account_id}:'
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
    import sys
    import os
    import settings

    dir_name = os.path.dirname(os.path.abspath(__file__))
    sys.path.append(os.path.dirname(dir_name))

    from services.aws.boto3_client_service import Boto3Client
    boto3_client = Boto3Client(
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY
    )
    lambda_test_client = boto3_client.get_lambda_client()
    s3_test_client = boto3_client.get_s3_client()

    create_triggers_and_destinations(
        lambda_client=lambda_test_client,
        s3_client=s3_test_client,
        region=settings.AWS_DEFAULT_REGION,
        aws_account_id=settings.AWS_ACCOUNT_ID,
        bucket_name=settings.AWS_BUCKET_NAMES.get('csv')
    )
