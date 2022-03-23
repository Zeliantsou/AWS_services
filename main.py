from time import sleep

import settings
from aws_boto3_client import Boto3Client
from create_buckets_1 import create_buckets
from generate_zips_lambda_2 import generate_zips_lambda
from upload_zips_to_s3_3 import upload_zips_to_s3
from create_role_and_policy_4 import create_role_and_policy
from create_lambda_functions_5 import create_lambda_functions
from create_api_gateway_6 import create_api_gateway
from create_triggers_and_destinations_7 import create_triggers_and_destinations
from aws_s3_bucket_services import upload_file_to_s3_bucket


def main():
    # 0. Get boto3 clients
    print('Stage - 0. Creating boto3 clients...')
    boto3_client = Boto3Client(
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY
    )
    s3_client = boto3_client.get_s3_client()
    iam_client = boto3_client.get_iam_client()
    lambda_client = boto3_client.get_lambda_client()
    api_gateway_client = boto3_client.get_api_gateway_client()
    sleep(2)
    print('Stage - 0. Boto clients are ready!')

    # 1. Create buckets for csv and lambda functions
    print('Stage - 1. Creating buckets for csv file and lambda functions...')
    create_buckets(s3_client=s3_client)
    sleep(5)
    print('Stage - 1. Buckets for zips and lambda are created')

    # 2. Generate zip files with code for lambda functions
    print('Stage - 2. Creating creating zip files with code for lambda functions...')
    generate_zips_lambda(
        directory_path_lambda=settings.DIRECTORY_PATH_LAMBDA,
        directory_path_zip_storage=settings.DIRECTORY_PATH_ZIP_STORAGE
    )
    sleep(2)
    print('Stage - 2. Zip files are generated')

    # 3. Upload zips for lambda functions to the bucket
    print('Stage - 3. Uploading zips for lambda functions to the bucket...')
    upload_zips_to_s3(
        s3_client=s3_client,
        directory_path_lambda=settings.DIRECTORY_PATH_LAMBDA,
        directory_path_zip_storage=settings.DIRECTORY_PATH_ZIP_STORAGE
    )
    sleep(2)
    print('Stage - 3. Zip files for lambda functions are uploaded')

    # 4 Create role with policies for lambda functions
    print('Stage - 4. Creating role and policies for lambda functions...')
    create_role_and_policy(
        iam_client=iam_client,
        role_name=settings.AWS_ROLE_NAME
    )
    sleep(20)
    print('Stage - 4. Role with policies for lambda functions is created')

    # 5 Create lambda functions
    print('Stage - 5. Creating lambda functions on AWS side...')
    create_lambda_functions(
        iam_client=iam_client,
        s3_client=s3_client,
        lambda_client=lambda_client
    )
    sleep(5)
    print('Stage - 5. Lambda functions on AWS side are created')

    # 6 Create api gateway
    print('Stage - 6. Creating API gateway...')
    create_api_gateway(
        api_gateway_client=api_gateway_client,
        lambda_client=lambda_client,
        api_stage_name=settings.AWS_API_STAGE_NAME
    )
    sleep(5)
    print('Stage - 6. Api gateway is created')

    # 7 Create triggers and destinations for lambda functions
    print('Stage - 7. Creating triggers for lambda functions...')
    try:
        create_triggers_and_destinations(
            lambda_client=lambda_client,
            s3_client=s3_client
        )
        sleep(5)
        print('Stage - 7. Triggers and destinations are created')
    except Exception:
        print('Triggers and destinations are not created. You should tweak it manually')
        pass

    # 8. Upload csv file to the bucket
    print('Stage - 8. Uploading csv file to the bucket...')
    upload_file_to_s3_bucket(
        s3_client=s3_client,
        file_path=settings.INITIAL_DB_DATA_PATH,
        bucket_name=settings.AWS_BUCKET_NAME_CSV,
        key=settings.FILE_NAME_IN_BUCKET
    )
    sleep(2)
    print('Stage - 8. CSV file is uploaded')


if __name__ == '__main__':
    main()
