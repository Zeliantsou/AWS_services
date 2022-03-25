
from services.aws.api_gateway_service import (
    create_rest_api,
    get_rest_api_id,
    get_resources,
    get_resource_id,
    add_rest_resource,
    add_integration_method,
    get_parent_id,
    deploy_api_gateway
)


def create_api_gateway(api_gateway_client, lambda_client,
                       api_stage_name, gateway_name,
                       resource_path, resource_methods,
                       aws_region, aws_account_id):
    create_rest_api(
        api_gateway_client=api_gateway_client,
        api_name=gateway_name
    )
    api_id = get_rest_api_id(
        api_gateway_client=api_gateway_client,
        api_name=gateway_name
    )
    resources = get_resources(
        api_gateway_client=api_gateway_client,
        api_id=api_id
    )
    parent_id = get_parent_id(resources=resources)
    new_resource = add_rest_resource(
        api_gateway_client=api_gateway_client,
        api_id=api_id,
        resource_path=resource_path,
        parent_id=parent_id
    )
    new_resource_id = get_resource_id(new_resource)
    for rest_method, lambda_func_name in resource_methods.items():
        add_integration_method(
            api_gateway_client=api_gateway_client,
            api_id=api_id,
            resource_id=new_resource_id,
            rest_method=rest_method,
            lambda_client=lambda_client,
            lambda_func_name=lambda_func_name,
            service_method='POST',
            aws_region=aws_region,
            aws_account_id=aws_account_id,
            resource_path=resource_path
        )
    deploy_api_gateway(
        api_gateway_client=api_gateway_client,
        api_id=api_id,
        stage_name=api_stage_name
    )


if __name__ == '__main__':
    import sys
    import os
    import settings
    from services.aws.boto3_client_service import Boto3Client

    dir_name = os.path.dirname(os.path.abspath(__file__))
    sys.path.append(os.path.dirname(dir_name))

    boto3_client = Boto3Client(
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY
    )
    api_gateway_test_client = boto3_client.get_api_gateway_client()
    iam_test_client = boto3_client.get_iam_client()
    s3_test_client = boto3_client.get_s3_client()
    lambda_test_client = boto3_client.get_lambda_client()

    create_api_gateway(
        api_gateway_client=api_gateway_test_client,
        lambda_client=lambda_test_client,
        api_stage_name=settings.AWS_API_STAGE_NAME,
        gateway_name=settings.AWS_API_GATEWAY_NAME,
        resource_path=settings.AWS_RESOURCE_PATH,
        resource_methods=settings.AWS_RESOURCE_METHODS,
        aws_region=settings.AWS_DEFAULT_REGION,
        aws_account_id=settings.AWS_ACCOUNT_ID
    )
