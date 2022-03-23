import boto3


table_name = 'cereal-zelentsov'
dynamo_db_client = boto3.client('dynamodb')


def lambda_handler(event, context):
    key = event['key']
    attribute_values = {k: v for k, v in key.items() if v}
    key_name = attribute_values.pop('name')
    key_mfr = attribute_values.pop('mfr')
    expression_attribute_names = {}
    expression_attribute_values = {}
    update_expression = 'SET '

    for key, value in attribute_values.items():
        key_upper_case = '#' + key.upper()
        expression_attribute_names[key_upper_case] = key
        expression_attribute_values[':' + key] = {
            'S' if key in ('name', 'mfr', 'type') else 'N': value
        }
        update_expression = update_expression + key_upper_case + ' = :' + key + ', '
    update_expression = update_expression[:len(update_expression)-2]
    updated_item = dynamo_db_client.update_item(
        ExpressionAttributeNames=expression_attribute_names,
        ExpressionAttributeValues=expression_attribute_values,
        Key={
            'name': {
                'S': key_name,
            },
            'mfr': {
                'S': key_mfr,
            },
        },
        ReturnValues='ALL_NEW',
        TableName=table_name,
        UpdateExpression=update_expression,
    )
    return {
        'statusCode': 200,
        'body': updated_item
    }
