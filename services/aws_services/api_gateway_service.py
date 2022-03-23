import json
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
    api_gateway_client.put_method(
        restApiId=api_id,
        resourceId=resource_id,
        httpMethod=rest_method,
        authorizationType="NONE",
        # apiKeyRequired=True,  # information from aws docs site
    )

    aws_region = settings.AWS_DEFAULT_REGION
    api_version = lambda_client.meta.service_model.api_version
    aws_account_id = settings.AWS_ACCOUNT_ID
    uri = (f'arn:aws:apigateway:{aws_region}:lambda:path/'
           f'{api_version}/functions/arn:aws:lambda:{aws_region}:'
           f'{aws_account_id}:function:{lambda_func_name}/invocations'
           )

    map_templ = {
        'key': {
            'name': "$input.params('name')",
            'mfr': "$input.params('mfr')",
        }
    }
    map_templ_update = {
        'key': {
            'name': "$input.params('name')",
            'mfr': "$input.params('mfr')",
            'calories': "$input.params('calories')",
            'carbo': "$input.params('carbo')",
            'cups': "$input.params('cups')",
            'fat': "$input.params('fat')",
            'fiber': "$input.params('fiber')",
            'potass': "$input.params('potass')",
            'protein': "$input.params('protein')",
            'rating': "$input.params('rating')",
            'shelf': "$input.params('shelf')",
            'sodium': "$input.params('sodium')",
            'sugar': "$input.params('sugar')",
            'type': "$input.params('type')",
            'vitamins': "$input.params('vitamins')",
            'weight': "$input.params('weight')",
        }
    }
    map_templ = json.dumps(map_templ)
    map_templ_update = json.dumps(map_templ_update)

    api_gateway_client.put_integration(
        restApiId=api_id,
        resourceId=resource_id,
        httpMethod=rest_method,
        type="AWS",
        integrationHttpMethod=service_method,
        requestTemplates={
            'application/json': map_templ_update if rest_method == 'PATCH' else map_templ
        },
        uri=uri,
    )

    api_gateway_client.put_integration_response(
        restApiId=api_id,
        resourceId=resource_id,
        httpMethod=rest_method,
        statusCode="200",
        selectionPattern=".*",
        responseTemplates={'application/json': ''},  # information from aws docs site
    )

    api_gateway_client.put_method_response(
        restApiId=api_id,
        resourceId=resource_id,
        httpMethod=rest_method,
        statusCode="200",
        responseModels={'application/json': 'Empty'},  # information from aws docs site
    )
    source_arn = (f'arn:aws:execute-api:{aws_region}:'
                  f'{aws_account_id}:{api_id}/*/'
                  f'{rest_method}/{settings.AWS_RESOURCE_PATH}'
                  )
    lambda_client.add_permission(
        FunctionName=lambda_func_name,
        StatementId=uuid.uuid4().hex,
        Action="lambda:InvokeFunction",
        Principal="apigateway.amazonaws.com",
        SourceArn=source_arn
    )


def deploy_api_gateway(api_gateway_client, api_id, stage_name):
    api_gateway_client.create_deployment(
        restApiId=api_id,
        stageName=stage_name
    )
