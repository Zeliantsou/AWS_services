import boto3


table_name = 'cereal-zelentsov'
dynamo_db_client = boto3.client('dynamodb')


def lambda_handler(event, context):
    key = event['key']
    name = key['name']
    mfr = key['mfr']
    deleted_item = dynamo_db_client.delete_item(
        Key={
            'name': {
                'S': name,
            },
            'mfr': {
                'S': mfr,
            },
        },
        TableName=table_name,
    )
    return {
        'statusCode': 200,
        'body': deleted_item
    }
