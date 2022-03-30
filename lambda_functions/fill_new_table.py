import json
import boto3
from urllib import parse

TABLE_NAME = 'cereal-zelentsov'


def batch_write_items(
        dynamo_db_client,
        table_name: str,
        data_list: list) -> dict:
    """
    Writes certain amount of items to the table.
    """
    return dynamo_db_client.batch_write_item(
        RequestItems={table_name: data_list}
    )


def put_items_into_db(
        dynamo_db_client,
        table_name: str,
        datalist: list):
    """
    Divides all the data into parts and conveys those
    part to the function for batch create.
    """
    is_items = True
    while is_items:
        if len(datalist) > 25:
            part_datalist = datalist[:25]
            del datalist[0:25]
            batch_write_items(dynamo_db_client, table_name, part_datalist)
        elif len(datalist) > 0:
            batch_write_items(dynamo_db_client, table_name, datalist)
            is_items = False


def lambda_handler(event, context):
    """
    Fill a newly created table with data.
    """
    dynamo_db_client = boto3.client('dynamodb')
    s3_client = boto3.client('s3')

    bucket_name = event['requestPayload']['requestPayload']['Records'][0]['s3']['bucket']['name']
    key = event['requestPayload']['requestPayload']['Records'][0]['s3']['object']['key']
    key = parse.unquote_plus(key, encoding='utf-8')
    bucket_object = s3_client.get_object(Bucket=bucket_name, Key=key)
    bucket_object = bucket_object['Body'].read().decode()

    parsed_data = bucket_object.splitlines()
    column_names = parsed_data.pop(0).split(',')
    str_type_column = ('name', 'mfr', 'type')
    items_data = []
    while len(parsed_data) != 0:
        row = parsed_data.pop(0).split(',')
        item = {}
        for column_name, value in zip(column_names, row):
            if column_name in str_type_column:
                item[column_name] = {'S': value}
            else:
                item[column_name] = {'N': value}
        items_data.append({'PutRequest': {'Item': item}})

    put_items_into_db(
        dynamo_db_client=dynamo_db_client,
        table_name=TABLE_NAME,
        datalist=items_data)

    return {
        'statusCode': 200,
        'body': json.dumps(f'Data from csv file is in the table "{TABLE_NAME}"')
    }
