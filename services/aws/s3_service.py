
def create_s3_bucket(
        s3_client,
        bucket_name: str,
        region: str
) -> dict:
    """
    Create S3 bucket.
    """
    location = {'LocationConstraint': region}
    return s3_client.create_bucket(
        Bucket=bucket_name,
        CreateBucketConfiguration=location
    )


def create_all_s3_buckets(create_one_bucket):
    """
    Decorator for creating all buckets.
    """
    def wrapper(dict_bucket_names, **kwargs):
        for bucket_name in dict_bucket_names.values():
            kwargs['bucket_name'] = bucket_name
            create_one_bucket(**kwargs)
    return wrapper


def upload_file_to_s3_bucket(
        s3_client,
        file_path: str,
        bucket_name: str,
        key: str
) -> None:
    """
    Uploads file to S3 bucket.
    """
    s3_client.upload_file(file_path, bucket_name, key)


def get_list_objects(
        s3_client,
        bucket_name: str) -> dict:
    """
    Gets list objects from the bucket.
    """
    return s3_client.list_objects(
        Bucket=bucket_name
    )


def get_key_objects(bucket_objects: dict) -> list:
    """
    Gets list object names from bucket objects.
    """
    keys = []
    for bucket_object in bucket_objects['Contents']:
        keys.append(bucket_object['Key'])
    return keys


def create_bucket_notification_configuration(
        s3_client,
        bucket_name: str,
        function_arn: str,
        events: list
) -> None:
    """
    Create notification for bucket and create a trigger
    for lambda function.
    """
    return s3_client.put_bucket_notification_configuration(
        Bucket=bucket_name,
        NotificationConfiguration={
            'LambdaFunctionConfigurations': [
                {'LambdaFunctionArn': function_arn,
                 'Events': events
                 }
            ]
        }
    )
