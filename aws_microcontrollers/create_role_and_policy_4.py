import settings
from aws_iam_services import (
    get_doc_provide_access_lambda,
    get_policy_json,
    create_policy_for_role,
    create_iam_role,
    attach_policy_to_role,
    get_list_policies
)


def create_role_and_policy(iam_client, role_name):
    role_policy_document = get_doc_provide_access_lambda()
    # policy_json = get_policy_json()
    # policy_role = create_policy_for_role(
    #     iam_client=iam_client,
    #     policy_name=policy_name,
    #     policy_document=policy_json
    # )
    # policy_arn = policy_role['Policy']['Arn']
    create_iam_role(
        iam_client=iam_client,
        role_name=role_name,
        role_policy_document=role_policy_document
    )
    for policy_arn in settings.AWS_DEFAULT_ARN_POLICIES:
        attach_policy_to_role(
            iam_client=iam_client,
            role_name=role_name,
            policy_arn=policy_arn  # policy_arn
        )


if __name__ == '__main__':
    from aws_boto3_client import Boto3Client
    boto_client = Boto3Client(
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY
    )
    iam_test_client = boto_client.get_iam_client()
    create_role_and_policy(
        iam_client=iam_test_client,
        role_name=settings.AWS_ROLE_NAME
    )
