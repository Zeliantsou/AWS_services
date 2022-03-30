import json
import boto3
from typing import List


TABLE_NAME = 'cereal-zelentsov'
HASH_COLUMN_NAME = 'name'
RANGE_COLUMN_NAME = 'mfr'
HASH_COLUMN_NAME_TYPE = 'S'
RANGE_COLUMN_NAME_TYPE = 'S'
READ_CAPACITY_UNITS = 10
WRITE_CAPACITY_UNITS = 10


def get_key_schema(
        hash_column_name: str,
        range_column_name: str) -> List[dict]:
    return [
        {
            'AttributeName': hash_column_name,
            'KeyType': 'HASH'
        },
        {
            'AttributeName': range_column_name,
            'KeyType': 'RANGE'
        },
    ]


def get_attribute_definitions(
        hash_column_name: str,
        hash_column_name_type: str,
        range_column_name: str,
        range_column_name_type: str
) -> List[dict]:
    return [
        {
            'AttributeName': hash_column_name,
            'AttributeType': hash_column_name_type
        },
        {
            'AttributeName': range_column_name,
            'AttributeType': range_column_name_type
        }
    ]


def get_provisioned_throughput(
        read_capacity_units: int,
        write_capacity_units: int) -> dict:
    return {
        'ReadCapacityUnits': read_capacity_units,
        'WriteCapacityUnits': write_capacity_units
    }


def lambda_handler(event, context):
    """
    Creates a new DynamoDB table to
    storage data about cereals.
    """
    dynamo_db_client = boto3.client('dynamodb')
    key_schema = get_key_schema(
        hash_column_name=HASH_COLUMN_NAME,
        range_column_name=RANGE_COLUMN_NAME
        )
    attribute_definitions = get_attribute_definitions(
        hash_column_name=HASH_COLUMN_NAME,
        hash_column_name_type=HASH_COLUMN_NAME_TYPE,
        range_column_name=RANGE_COLUMN_NAME,
        range_column_name_type=RANGE_COLUMN_NAME_TYPE
        )
    provisioned_throughput = get_provisioned_throughput(
        read_capacity_units=READ_CAPACITY_UNITS,
        write_capacity_units=WRITE_CAPACITY_UNITS
        )
    dynamo_db_client.create_table(
            TableName=TABLE_NAME,
            KeySchema=key_schema,
            AttributeDefinitions=attribute_definitions,
            ProvisionedThroughput=provisioned_throughput
        )
    return {
        'statusCode': 200,
        'body': json.dumps(f'Table {TABLE_NAME} is created')
    }
