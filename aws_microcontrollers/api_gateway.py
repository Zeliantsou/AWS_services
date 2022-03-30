
import logging

from botocore.exceptions import ClientError

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


logger = logging.getLogger(__name__)


def create_api_gateway(
        api_gateway_client,
        lambda_client: str,
        api_stage_name: str,
        gateway_name: str,
        resource_path: str,
        resource_methods: dict,
        aws_region: str,
        aws_account_id: str
) -> None:
    """
    Creates API gateway, adds one resource and
    default methods, deploys API.
    """
    try:
        create_rest_api(
            api_gateway_client=api_gateway_client,
            api_name=gateway_name
        )
    except ClientError:
        logger.exception(
            f'Could not create REST api with name "{gateway_name}"')
        raise
    api_id = get_rest_api_id(
        api_gateway_client=api_gateway_client,
        api_name=gateway_name
    )
    try:
        resources = get_resources(
            api_gateway_client=api_gateway_client,
            api_id=api_id
        )
    except ClientError:
        logger.exception(
            f'Could not get resources from api with id {api_id}')
        raise
    parent_id = get_parent_id(resources=resources)
    try:
        new_resource = add_rest_resource(
            api_gateway_client=api_gateway_client,
            api_id=api_id,
            resource_path=resource_path,
            parent_id=parent_id
        )
    except ClientError:
        logger.exception(
            f'Could not create a new resource "{resource_path}"')
        raise
    new_resource_id = get_resource_id(new_resource)
    for rest_method, lambda_func_name in resource_methods.items():
        try:
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
        except ClientError:
            logger.exception(
                f'Could not add integration method "{rest_method}"')
            raise
    try:
        deploy_api_gateway(
            api_gateway_client=api_gateway_client,
            api_id=api_id,
            stage_name=api_stage_name
        )
    except ClientError:
        logger.exception(
            f'Could not deploy api gateway with id "{api_id}"')
        raise
