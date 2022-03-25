
def create_s3_bucket(s3_client, bucket_name, region):
    location = {'LocationConstraint': region}
    s3_client.create_bucket(
        Bucket=bucket_name,
        CreateBucketConfiguration=location
    )


def create_all_s3_buckets(create_one_bucket):
    def wrapper(dict_bucket_names, **kwargs):
        for bucket_name in dict_bucket_names.values():
            kwargs['bucket_name'] = bucket_name
            create_one_bucket(**kwargs)
    return wrapper


def upload_file_to_s3_bucket(s3_client, file_path,
                             bucket_name, key):
    s3_client.upload_file(file_path, bucket_name, key)


def get_list_objects(s3_client, bucket_name,):
    return s3_client.list_objects(
        Bucket=bucket_name
    )


def get_key_objects(bucket_objects):
    keys = []
    for bucket_object in bucket_objects['Contents']:
        keys.append(bucket_object['Key'])
    return keys


def create_bucket_notification_configuration(
        s3_client, bucket_name, function_arn, events):
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
