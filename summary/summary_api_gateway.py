import uuid
import settings


def create_rest_api(api_gateway_client, api_name):
    rest_api = api_gateway_client.create_rest_api(
        name=api_name)
    return rest_api['id']


def get_rest_api_id(api_gateway_client, api_name):
    rest_api = None
    paginator = api_gateway_client.get_paginator(
        'get_rest_apis')
    for page in paginator.paginate():
        rest_api = next(
            (item for item in page['items'] if item['name'] == api_name), None)
        if rest_api is not None:
            break
    return rest_api['id']


def get_resources(api_gateway_client, api_id):
    return api_gateway_client.get_resources(
        restApiId=api_id)


def get_parent_id(resources):
    return resources['items'][0]['id']


def add_rest_resource(api_gateway_client, api_id,
                      resource_path, parent_id):
    resource = api_gateway_client.create_resource(
        restApiId=api_id,
        pathPart=resource_path,
        parentId=parent_id
    )
    return resource


def get_resource_id(resource):
    return resource['id']


def add_integration_method(api_gateway_client, api_id,
                           resource_id, rest_method,
                           lambda_client, lambda_func_name,
                           service_method):
    put_method_resp = api_gateway_client.put_method(
        restApiId=api_id,
        resourceId=resource_id,
        httpMethod=rest_method,
        authorizationType="NONE",
        apiKeyRequired=True,
    )

    aws_region = settings.AWS_DEFAULT_REGION
    api_version = lambda_client.meta.service_model.api_version
    aws_account_id = settings.AWS_ACCOUNT_ID

    uri = (f'arn:aws:apigateway:{aws_region}:lambda:path/'
           f'{api_version}/functions/arn:aws:lambda:{aws_region}:'
           f'{aws_account_id}:function:{lambda_func_name}/invocations'
           )
    integration_resp = api_gateway_client.put_integration(
        restApiId=api_id,
        resourceId=resource_id,
        httpMethod=rest_method,
        type="AWS",
        integrationHttpMethod=service_method,
        uri=uri,
    )
    api_gateway_client.put_integration_response(
        restApiId=api_id,
        resourceId=resource_id,
        httpMethod=rest_method,
        statusCode="200",
        selectionPattern=".*"
    )
    api_gateway_client.put_method_response(
        restApiId=api_id,
        resourceId=resource_id,
        httpMethod=rest_method,
        statusCode="200",
    )

    source_arn = (f'arn:aws:execute-api:{aws_region}:'
                  f'{aws_account_id}:{api_id}/*/'
                  f'{rest_method}/{lambda_func_name}'
                  )

    lambda_client.add_permission(
        FunctionName=lambda_func_name,
        StatementId=uuid.uuid4().hex,
        Action="lambda:InvokeFunction",
        Principal="apigateway.amazonaws.com",
        SourceArn=source_arn
    )

    # service_uri = (
    #     f'arn:aws:apigateway:{api_gateway_client.meta.region_name}'
    #     f':{service_endpoint_prefix}:path/{api_gateway_client.meta.service_model.api_version}'
    #     f'/functions/{service_action}/invocations'
    # )
    # service_uri = (
    #     f'arn:aws:apigateway:{api_gateway_client.meta.region_name}'
    #     f':{service_endpoint_prefix}:action/{service_action}'
    # )
    # api_gateway_client.put_method(
    #     restApiId=api_id,
    #     resourceId=resource_id,
    #     httpMethod=rest_method,
    #     authorizationType='NONE')
    # api_gateway_client.put_integration(
    #     restApiId=api_id,
    #     resourceId=resource_id,
    #     httpMethod=rest_method,
    #     type='AWS',
    #     integrationHttpMethod=service_method,
    #     # credentials=role_arn,
    #     uri=service_uri,
    #     passthroughBehavior='WHEN_NO_TEMPLATES')
    # api_gateway_client.put_integration_response(
    #     restApiId=api_id,
    #     resourceId=resource_id,
    #     httpMethod=rest_method,
    #     statusCode='200',
    #     responseTemplates={'application/json': ''})
    # api_gateway_client.put_method_response(
    #     restApiId=api_id,
    #     resourceId=resource_id,
    #     httpMethod=rest_method,
    #     statusCode='200',
    #     responseModels={'application/json': 'Empty'})

    # api_gateway_client.put_method(
    #     restApiId=api_id,
    #     resourceId=resource_id,
    #     httpMethod=rest_method,
    #     authorizationType='NONE')
    # api_gateway_client.put_method_response(
    #     restApiId=api_id,
    #     resourceId=resource_id,
    #     httpMethod=rest_method,
    #     statusCode='200',
    #     responseModels={'application/json': 'Empty'})
    # api_gateway_client.put_integration(
    #     restApiId=api_id,
    #     resourceId=resource_id,
    #     httpMethod=rest_method,
    #     type='AWS',
    #     integrationHttpMethod=service_method,
    #     credentials=role_arn,
    #     uri=service_uri,
    #     passthroughBehavior='WHEN_NO_TEMPLATES')
    # api_gateway_client.put_integration_response(
    #     restApiId=api_id,
    #     resourceId=resource_id,
    #     httpMethod=rest_method,
    #     statusCode='200',
    #     responseTemplates={'application/json': ''})


def deploy_api_gateway(api_gateway_client, api_id, stage_name):
    api_gateway_client.create_deployment(
        restApiId=api_id,
        stageName=stage_name
    )
    url = (f'https://{api_id}.execute-api.{api_gateway_client.meta.region_name}'
           f'.amazonaws.com/{stage_name}')
    return url
