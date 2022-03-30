
import logging
import uuid
from typing import Sequence

from botocore.exceptions import ClientError

from services.aws.lambda_service import (
    add_permission_for_lambda,
    get_policy_for_lambda,
    create_destination_for_lambda,
    get_lambda_arn,
    get_source_arn,
)
from services.aws.s3_service import (
    create_bucket_notification_configuration)


logger = logging.getLogger(__name__)


def create_triggers_and_destinations(
        lambda_client,
        s3_client,
        region: str,
        aws_account_id: str,
        bucket_name: str,
        lambda_destinations: Sequence[dict]
):
    """
    Creates trigger for lambda function that start
    working with DynamoDB after uploading csv file to
    the bucket and also creates destinations for
    functions.
    """
    function_with_trigger_arn = get_lambda_arn(
        region=region,
        aws_account_id=aws_account_id,
        function_name='delete_existing_table'
    )
    source_arn = get_source_arn(bucket_name=bucket_name)

    try:
        add_permission_for_lambda(
            lambda_client=lambda_client,
            action='lambda:InvokeFunction',
            function_name=function_with_trigger_arn,
            principal='s3.amazonaws.com',
            source_arn=source_arn,
            statement_id=uuid.uuid4().hex
        )
    except ClientError:
        logger.exception(
            (f'Could not add permission for'
             f'lambda function "{function_with_trigger_arn}"')
        )
        raise
    try:
        get_policy_for_lambda(
            lambda_client=lambda_client,
            function_arn=function_with_trigger_arn
        )
    except ClientError:
        logger.exception(
            (f'Could not get policy for'
             f'lambda function "{function_with_trigger_arn}"')
        )
        raise
    try:
        create_bucket_notification_configuration(
            s3_client=s3_client,
            bucket_name=bucket_name,
            function_arn=function_with_trigger_arn,
            events=['s3:ObjectCreated:Put']
        )
    except ClientError:
        logger.exception(
            (f'Could not create notification configuration'
             f'for bucket "{bucket_name}"')
        )
        raise
    for lambda_function in lambda_destinations:
        function_name = lambda_function.get('function_name')
        destin_func_name = lambda_function.get(
            'destination_function_name')
        destin_func_arn = get_lambda_arn(
            region=region,
            aws_account_id=aws_account_id,
            function_name=destin_func_name
        )
        try:
            create_destination_for_lambda(
                lambda_client=lambda_client,
                function_name=function_name,
                destination_arn=destin_func_arn
            )
        except ClientError:
            logger.exception(
                (f'Could not create destination for'
                 f'lambda function "{function_name}"')
            )
            raise
