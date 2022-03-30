
import logging

from botocore.exceptions import ClientError

from services.aws.iam_service import get_iam_role_arn
from services.aws.s3_service import (
    get_list_objects,
    get_key_objects
)
from services.aws.lambda_service import (
    create_lambda_function,
    get_lambda_function_name,
    get_lambda_handler
)


logger = logging.getLogger(__name__)


def create_lambda_functions(
        iam_client,
        s3_client,
        lambda_client,
        role_name: str,
        bucket_name_lambda: str
) -> None:
    """
    Create all lambda functions on AWS side.
    """
    try:
        role_arn = get_iam_role_arn(
            iam_client=iam_client,
            role_name=role_name
        )
    except ClientError:
        logger.exception(
            f'Could not get role arn from role name "{role_name}"')
        raise
    try:
        bucket_objects = get_list_objects(
            s3_client=s3_client,
            bucket_name=bucket_name_lambda
        )
    except ClientError:
        logger.exception(
            (f'Could not get list of objects from'
             f'bucket "{bucket_name_lambda}"')
        )
        raise
    keys = get_key_objects(bucket_objects)
    for key in keys:
        code_data = {
            'S3Bucket': bucket_name_lambda,
            'S3Key': key,
        }
        function_name = get_lambda_function_name(key)
        try:
            create_lambda_function(
                lambda_client=lambda_client,
                code_data=code_data,
                function_name=function_name,
                role_arn=role_arn,
                handler=get_lambda_handler(key)
            )
        except ClientError:
            logger.exception(
                (f'Could not create lambda function'
                 f'with name "{function_name}"')
            )
            raise
