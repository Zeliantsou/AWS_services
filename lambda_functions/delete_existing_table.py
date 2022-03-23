import json
import boto3

TABLE_NAME = 'cereal-zelentsov'


def lambda_handler(event, context):
    dynamo_db_client = boto3.client(
        'dynamodb',
        aws_access_key_id='AKIAQ3POWT3O3A64G2VO',
        aws_secret_access_key='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'
    )
    tables = dynamo_db_client.list_tables()
    if TABLE_NAME in tables['TableNames']:
        dynamo_db_client.delete_table(
            TableName=TABLE_NAME)
        print(f'table {TABLE_NAME} has been deleted')

    return {
        'statusCode': 200,
        'body': json.dumps(f'Table {TABLE_NAME} does not already exist')
    }
