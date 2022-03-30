
import logging
from time import sleep

import settings
from services.aws.boto3_client_service import Boto3Client
from aws_microcontrollers.buckets import create_buckets
from aws_microcontrollers.lambda_zips import generate_lambda_zips
from aws_microcontrollers.zips_to_s3 import upload_zips_to_s3
from aws_microcontrollers.role_and_policy import create_role_and_policy
from aws_microcontrollers.lambda_functions import create_lambda_functions
from aws_microcontrollers.api_gateway import create_api_gateway
from aws_microcontrollers.triggers_and_destinations import (
    create_triggers_and_destinations)
from aws_microcontrollers.csv_to_s3 import upload_to_s3


def main():
    logging.basicConfig(filename='log.log')

    # 0. Get boto3 clients
    boto3_client = Boto3Client(
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY
    )
    s3_client = boto3_client.get_s3_client()
    iam_client = boto3_client.get_iam_client()
    lambda_client = boto3_client.get_lambda_client()
    api_gateway_client = boto3_client.get_api_gateway_client()

    # 1. Create buckets for csv and lambda functions
    create_buckets(
        dict_bucket_names=settings.AWS_BUCKET_NAMES,
        s3_client=s3_client,
        region=settings.AWS_DEFAULT_REGION
    )
    sleep(5)

    # 2. Generate zip files with code for lambda functions
    generate_lambda_zips(
        directory_path_lambda=settings.DIRECTORY_PATH_LAMBDA,
        directory_path_zip_storage=settings.DIRECTORY_PATH_ZIP_STORAGE
    )

    # 3. Upload zips for lambda functions to the bucket
    upload_zips_to_s3(
        s3_client=s3_client,
        directory_path_lambda=settings.DIRECTORY_PATH_LAMBDA,
        directory_path_zip_storage=settings.DIRECTORY_PATH_ZIP_STORAGE,
        bucket_name=settings.AWS_BUCKET_NAMES.get('lambda')
    )
    sleep(5)

    # 4 Create role with policies for lambda functions
    create_role_and_policy(
        iam_client=iam_client,
        role_name=settings.AWS_ROLE_NAME,
        arn_policies=settings.AWS_DEFAULT_ARN_POLICIES
    )
    sleep(20)

    # 5 Create lambda functions on AWS side
    create_lambda_functions(
        iam_client=iam_client,
        s3_client=s3_client,
        lambda_client=lambda_client,
        role_name=settings.AWS_ROLE_NAME,
        bucket_name_lambda=settings.AWS_BUCKET_NAMES.get('lambda')
    )
    sleep(5)

    # 6 Create api gateway
    create_api_gateway(
        api_gateway_client=api_gateway_client,
        lambda_client=lambda_client,
        api_stage_name=settings.AWS_API_STAGE_NAME,
        gateway_name=settings.AWS_API_GATEWAY_NAME,
        resource_path=settings.AWS_RESOURCE_PATH,
        resource_methods=settings.AWS_RESOURCE_METHODS,
        aws_region=settings.AWS_DEFAULT_REGION,
        aws_account_id=settings.AWS_ACCOUNT_ID
    )
    sleep(5)

    # 7 Create triggers and destinations for lambda functions
    create_triggers_and_destinations(
        lambda_client=lambda_client,
        s3_client=s3_client,
        region=settings.AWS_DEFAULT_REGION,
        aws_account_id=settings.AWS_ACCOUNT_ID,
        bucket_name=settings.AWS_BUCKET_NAMES.get('csv'),
        lambda_destinations=settings.AWS_LAMBDA_DESTINATIONS,
    )
    sleep(5)

    # 8. Upload csv file to the bucket
    upload_to_s3(
        s3_client=s3_client,
        file_path=settings.INITIAL_DB_DATA_PATH,
        bucket_name=settings.AWS_BUCKET_NAMES.get('csv'),
        key=settings.FILE_NAME_IN_BUCKET
    )


if __name__ == '__main__':
    main()
