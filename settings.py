import os

from dotenv import load_dotenv


load_dotenv()

AWS_ACCOUNT_ID = os.environ.get('AWS_ACCOUNT_ID')
AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
AWS_DEFAULT_REGION = os.environ.get('AWS_DEFAULT_REGION')
AWS_STORAGE_BUCKET_NAME = os.environ.get('AWS_STORAGE_BUCKET_NAME')

AWS_BUCKET_NAMES = {
    'csv': 'cereal-zelentsov-csv',
    'lambda': 'cereal-zelentsov-lambda',
}
AWS_ROLE_NAME = 'cereal-zelentsov-role'
AWS_POLICY_NAME = 'cereal-zelentsov-policy'
AWS_API_GATEWAY_NAME = 'cereal-zelentsov-api'
AWS_RESOURCE_PATH = 'cereal'
AWS_RESOURCE_METHODS = {
    'POST': 'item_create',
    'GET': 'item_get',
    'PATCH': 'item_update',
    'DELETE': 'item_delete',
}
AWS_DEFAULT_ARN_POLICIES = (
    'arn:aws:iam::aws:policy/AmazonS3FullAccess',
    'arn:aws:iam::aws:policy/AmazonDynamoDBFullAccess',
    'arn:aws:iam::aws:policy/AWSOpsWorksCloudWatchLogs',
    'arn:aws:iam::aws:policy/AWSLambda_FullAccess',
    )
AWS_API_STAGE_NAME = 'test_stage'


DIRECTORY_PATH_LAMBDA = 'lambda_functions/'
DIRECTORY_PATH_ZIP_STORAGE = 'lambda_zips_for_aws /'
INITIAL_DB_DATA_PATH = 'db_initial_data/cereal.csv'
FILE_NAME_IN_BUCKET = 'cereal.csv'
