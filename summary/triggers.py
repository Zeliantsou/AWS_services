
from test_package.test_package_module import test_def


test_def()

# from time import sleep
#
# import boto3
#
# import settings
#
# lambda_client = boto3.client(
#     'lambda',
#     aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
#     aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY
# )
# s3_client = boto3.client(
#     's3',
#     aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
#     aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY
# )


# response = lambda_client.put_function_event_invoke_config(
#     FunctionName='delete_existing_table',
#     MaximumRetryAttempts=0,
#     MaximumEventAgeInSeconds=3600,
#     DestinationConfig={
#         'OnSuccess': {
#             'Destination': 'arn:aws:lambda:eu-central-1:059019534045:function:create_new_table'
#         },
#         'OnFailure': {
#
#         }
#     }
# )

# lambda_client.add_permission(FunctionName='arn:aws:lambda:eu-central-1:059019534045:function:delete_existing_table',
#                              StatementId='response2-id-2',
#                              Action='lambda:InvokeFunction',
#                              Principal='s3.amazonaws.com',
#                              SourceArn='arn:aws:s3:::cereal-zelentsov-csv'
#                              )
#
# lambda_client.get_policy(FunctionName='arn:aws:lambda:eu-central-1:059019534045:function:delete_existing_table')
# s3_client.put_bucket_notification_configuration(
#     Bucket='cereal-zelentsov-csv',
#     NotificationConfiguration={
#         'LambdaFunctionConfigurations': [
#             {'LambdaFunctionArn': 'arn:aws:lambda:eu-central-1:059019534045:function:delete_existing_table',
#              'Events': ['s3:ObjectCreated:*']
#              }
#         ]
#     }
# )
# response = lambda_client.remove_permission(
#     FunctionName='delete_existing_table',
#     StatementId='s33',
# )
# lambda_client = boto3.client(
#     'lambda',
#     aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
#     aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY
# )
