
def create_lambda_function(
        lambda_client,
        code_data: dict,
        function_name: str,
        role_arn: str,
        handler: str
) -> dict:
    """
    Creates lambda function.
    """
    return lambda_client.create_function(
        Code=code_data,
        FunctionName=function_name,
        Handler=handler,  # handler.py (certain file)
        Publish=True,
        Role=role_arn,
        Runtime='python3.8',
        )


def get_lambda_function_name(key: str) -> str:
    """
    Gets lambda function name.
    """
    return key.split('.')[0]


def get_lambda_handler(key: str) -> str:
    """
    Gets handler name for lambda function.
    """
    return key.split('.')[0] + '.lambda_handler'


def add_permission_for_lambda(
        lambda_client,
        action: str,
        function_name: str,
        principal: str,
        source_arn: str,
        statement_id: str
) -> dict:
    """
    Adds permission for lambda function.
    """
    return lambda_client.add_permission(
        Action=action,
        FunctionName=function_name,
        Principal=principal,
        SourceArn=source_arn,
        StatementId=statement_id,
    )


def get_policy_for_lambda(
        lambda_client,
        function_arn: str) -> dict:
    """
    Gets policy for lambda function.
    """
    return lambda_client.get_policy(FunctionName=function_arn)


def create_destination_for_lambda(
        lambda_client,
        function_name: str,
        destination_arn: str
) -> dict:
    """
    Create destination for lambda function.
    """
    return lambda_client.put_function_event_invoke_config(
        FunctionName=function_name,
        MaximumRetryAttempts=0,
        MaximumEventAgeInSeconds=3600,
        DestinationConfig={
            'OnSuccess': {
                'Destination': destination_arn
            },
            'OnFailure': {
            }
        }
    )


def get_lambda_arn(
        region: str,
        aws_account_id: str,
        function_name: str
) -> str:
    """
    Creates ARN for lambda function.
    """
    return (f'arn:aws:lambda:{region}:'
            f'{aws_account_id}:'
            f'function:{function_name}')


def get_source_arn(bucket_name: str) -> str:
    """
    Creates ARN for bucket.
    """
    return f'arn:aws:s3:::{bucket_name}'
