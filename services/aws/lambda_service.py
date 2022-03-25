
def create_lambda_function(lambda_client, code_data, function_name,
                           role_arn, handler):
    """
    e.g. Handler='handler.new_lambda_handler'
    handler - file (handler.py)
    new_lambda_handler - the name of the function in the handler.py
    """
    lambda_client.create_function(
        # Code=dict(ZipFile=code_data),
        Code=code_data,
        FunctionName=function_name,
        Handler=handler,
        Publish=True,
        Role=role_arn,
        Runtime='python3.8',
        )


def get_lambda_function_name(key):
    return key.split('.')[0]


def get_lambda_handler(key):
    return key.split('.')[0] + '.lambda_handler'


def add_permission_for_lambda(lambda_client, action, function_name,
                              principal, source_arn, statement_id):
    return lambda_client.add_permission(
        Action=action,
        FunctionName=function_name,
        Principal=principal,
        SourceArn=source_arn,
        StatementId=statement_id,
    )


def get_policy_for_lambda(lambda_client, function_arn):
    return lambda_client.get_policy(FunctionName=function_arn)


def create_destination_for_lambda(lambda_client, function_name,
                                  destination_arn):
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
