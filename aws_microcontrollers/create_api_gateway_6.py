
import settings
from aws_api_gateway_services import (
    create_rest_api,
    get_rest_api_id,
    get_resources,
    get_resource_id,
    add_rest_resource,
    add_integration_method,
    get_parent_id,
    deploy_api_gateway
)


def create_api_gateway(api_gateway_client, lambda_client, api_stage_name):
    """
    parent_id --> get from aws_api_gateway_services.get_resources method
    by api id. There were items. The only one id and that value we use.
    """
    create_rest_api(
        api_gateway_client=api_gateway_client,
        api_name=settings.AWS_API_GATEWAY_NAME
    )
    api_id = get_rest_api_id(
        api_gateway_client=api_gateway_client,
        api_name=settings.AWS_API_GATEWAY_NAME
    )
    resources = get_resources(
        api_gateway_client=api_gateway_client,
        api_id=api_id
    )
    parent_id = get_parent_id(resources=resources)
    new_resource = add_rest_resource(
        api_gateway_client=api_gateway_client,
        api_id=api_id,
        resource_path=settings.AWS_RESOURCE_PATH,
        parent_id=parent_id
    )
    new_resource_id = get_resource_id(new_resource)
    for rest_method, lambda_func_name in settings.AWS_RESOURCE_METHODS.items():
        add_integration_method(
            api_gateway_client=api_gateway_client,
            api_id=api_id,
            resource_id=new_resource_id,
            rest_method=rest_method,
            lambda_client=lambda_client,
            lambda_func_name=lambda_func_name,
            service_method='POST',
        )

    deploy_api_gateway(
        api_gateway_client=api_gateway_client,
        api_id=api_id,
        stage_name=api_stage_name
    )


if __name__ == '__main__':
    from aws_boto3_client import Boto3Client
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
        api_stage_name=settings.AWS_API_STAGE_NAME
    )
