import boto3


class Boto3Client:
    """
    Encapsulates all mandatory clients.
    """
    def __init__(self, aws_access_key_id, aws_secret_access_key):
        self.aws_access_key_id = aws_access_key_id
        self.aws_secret_access_key = aws_secret_access_key

    def get_s3_client(self):
        """
        Gets S3 client.
        """
        return boto3.client(service_name='s3',
                            aws_access_key_id=self.aws_access_key_id,
                            aws_secret_access_key=self.aws_secret_access_key)

    def get_iam_client(self):
        """
        Gets IAM client.
        """
        return boto3.client(service_name='iam',
                            aws_access_key_id=self.aws_access_key_id,
                            aws_secret_access_key=self.aws_secret_access_key)

    def get_lambda_client(self):
        """
        Gets lambda client.
        """
        return boto3.client(service_name='lambda',
                            aws_access_key_id=self.aws_access_key_id,
                            aws_secret_access_key=self.aws_secret_access_key)

    def get_api_gateway_client(self):
        """
        Gets api gateway client.
        """
        return boto3.client(service_name='apigateway',
                            aws_access_key_id=self.aws_access_key_id,
                            aws_secret_access_key=self.aws_secret_access_key)
