
from services.aws.iam_service import (
    create_iam_role,
    attach_policy_to_role,
)
from services.aws.values import get_doc_provide_access_lambda


def create_role_and_policy(iam_client, role_name, arn_policies):
    role_policy_document = get_doc_provide_access_lambda()
    create_iam_role(
        iam_client=iam_client,
        role_name=role_name,
        role_policy_document=role_policy_document
    )
    for policy_arn in arn_policies:
        attach_policy_to_role(
            iam_client=iam_client,
            role_name=role_name,
            policy_arn=policy_arn
        )


if __name__ == '__main__':
    import sys
    import os
    import settings
    from services.aws.boto3_client_service import Boto3Client

    dir_name = os.path.dirname(os.path.abspath(__file__))
    sys.path.append(os.path.dirname(dir_name))

    boto_client = Boto3Client(
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY
    )
    iam_test_client = boto_client.get_iam_client()
    role_policy_doc = get_doc_provide_access_lambda()
    create_role_and_policy(
        iam_client=iam_test_client,
        role_name=settings.AWS_ROLE_NAME,
        arn_policies=settings.AWS_DEFAULT_ARN_POLICIES
    )
