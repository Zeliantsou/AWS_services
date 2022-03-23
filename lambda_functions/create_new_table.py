import json
import boto3


TABLE_NAME = 'cereal-zelentsov'
HASH_COLUMN_NAME = 'name'
RANGE_COLUMN_NAME = 'mfr'
HASH_COLUMN_NAME_TYPE = 'S'
RANGE_COLUMN_NAME_TYPE = 'S'
READ_CAPACITY_UNITS = 10
WRITE_CAPACITY_UNITS = 10


def get_key_schema(hash_column_name, range_column_name):
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


def get_attribute_definitions(hash_column_name,
                              hash_column_name_type,
                              range_column_name,
                              range_column_name_type):
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


def get_provisioned_throughput(read_capacity_units,
                               write_capacity_units):
    return {
        'ReadCapacityUnits': read_capacity_units,
        'WriteCapacityUnits': write_capacity_units
    }


def lambda_handler(event, context):
    dynamo_db_client = boto3.client(
        'dynamodb',
        aws_access_key_id='AKIAQ3POWT3O3A64G2VO',
        aws_secret_access_key='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'
        )
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
