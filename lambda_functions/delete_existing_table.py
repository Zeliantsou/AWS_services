import json
import boto3

TABLE_NAME = 'cereal-zelentsov'


def lambda_handler(event, context):
    """
    Delete table for cereals if it exists.
    """
    dynamo_db_client = boto3.client('dynamodb')
    tables = dynamo_db_client.list_tables()
    if TABLE_NAME in tables['TableNames']:
        dynamo_db_client.delete_table(
            TableName=TABLE_NAME)
        print(f'table {TABLE_NAME} has been deleted')

    return {
        'statusCode': 200,
        'body': json.dumps(f'Table {TABLE_NAME} has been deleted')
    }
