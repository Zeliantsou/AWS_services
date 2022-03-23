import boto3


table_name = 'cereal-zelentsov'
dynamo_db_client = boto3.client('dynamodb')


def lambda_handler(event, context):
    key = event['key']
    name = key['name']
    mfr = key['mfr']
    item = dynamo_db_client.put_item(
        Item={
            'name': {
                'S': name,
            },
            'mfr': {
                'S': mfr,
            },
        },
        ReturnConsumedCapacity='TOTAL',
        TableName=table_name,
    )
    return {
        'statusCode': 201,
        'body': f"item with name '{name}', mfr '{mfr}' is created"
    }
