import uuid

from services.aws.values import (
    get_mapping_template,
    get_mapping_template_update
)


def create_rest_api(
        api_gateway_client,
        api_name: str) -> str:
    """
    Creates a REST API on API Gateway.
    """
    rest_api = api_gateway_client.create_rest_api(
        name=api_name)
    return rest_api['id']


def get_rest_api_id(
        api_gateway_client,
        api_name: str) -> str:
    """
    Gets REST API id.
    """
    rest_api = None
    paginator = api_gateway_client.get_paginator(
        'get_rest_apis')
    for page in paginator.paginate():
        rest_api = next(
            (item for item in page['items']
             if item['name'] == api_name), None
        )
        if rest_api is not None:
            break
    return rest_api['id']


def get_resources(
        api_gateway_client,
        api_id: str) -> dict:
    """
    Lists information about a collection of resources.
    """
    return api_gateway_client.get_resources(
        restApiId=api_id)


def get_parent_id(resources: dict) -> str:
    """
    Gets parent id for the first created resource
    for newly created API.
    """
    return resources['items'][0]['id']


def add_rest_resource(
        api_gateway_client,
        api_id: str,
        resource_path: str,
        parent_id: str
) -> dict:
    """
    Adds a new resource for REST api.
    """
    return api_gateway_client.create_resource(
        restApiId=api_id,
        pathPart=resource_path,
        parentId=parent_id
    )


def get_resource_id(resource: dict) -> str:
    """
    Gets id of resource.
    """
    return resource['id']


def add_integration_method(
        api_gateway_client,
        api_id: str,
        resource_id: str,
        rest_method: str,
        lambda_client,
        lambda_func_name: str,
        service_method: str,
        aws_region: str,
        aws_account_id: str,
        resource_path: str,
) -> None:
    """
    Adds an integration method to a REST api.
    """
    api_gateway_client.put_method(
        restApiId=api_id,
        resourceId=resource_id,
        httpMethod=rest_method,
        authorizationType="NONE",
        # apiKeyRequired=True,
    )
    api_version = lambda_client.meta.service_model.api_version
    uri = (f'arn:aws:apigateway:{aws_region}:lambda:path/'
           f'{api_version}/functions/arn:aws:lambda:{aws_region}:'
           f'{aws_account_id}:function:{lambda_func_name}/invocations'
           )
    map_templ = get_mapping_template()
    map_templ_update = get_mapping_template_update()
    api_gateway_client.put_integration(
        restApiId=api_id,
        resourceId=resource_id,
        httpMethod=rest_method,
        type="AWS",
        integrationHttpMethod=service_method,
        requestTemplates={
            'application/json': map_templ_update
            if rest_method == 'PATCH'
            else map_templ
        },
        uri=uri,
    )
    api_gateway_client.put_integration_response(
        restApiId=api_id,
        resourceId=resource_id,
        httpMethod=rest_method,
        statusCode="200",
        selectionPattern=".*",
        responseTemplates={'application/json': ''},
    )
    api_gateway_client.put_method_response(
        restApiId=api_id,
        resourceId=resource_id,
        httpMethod=rest_method,
        statusCode="200",
        responseModels={'application/json': 'Empty'},
    )
    source_arn = (f'arn:aws:execute-api:{aws_region}:'
                  f'{aws_account_id}:{api_id}/*/'
                  f'{rest_method}/{resource_path}'
                  )
    lambda_client.add_permission(
        FunctionName=lambda_func_name,
        StatementId=uuid.uuid4().hex,
        Action="lambda:InvokeFunction",
        Principal="apigateway.amazonaws.com",
        SourceArn=source_arn
    )


def deploy_api_gateway(
        api_gateway_client,
        api_id: str,
        stage_name: str
) -> dict:
    """
    Deploys a REST api.
    """
    return api_gateway_client.create_deployment(
        restApiId=api_id,
        stageName=stage_name
    )
