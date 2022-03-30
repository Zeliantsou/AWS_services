
def create_iam_role(
        iam_client,
        role_name: str,
        role_policy_document: str
) -> dict:
    """
    Creates IAM role by policy document.
    """
    return iam_client.create_role(
        RoleName=role_name,
        AssumeRolePolicyDocument=role_policy_document,
    )


def get_iam_role(
        iam_client,
        role_name: str) -> dict:
    """
    Gets IAM role by role name.
    """
    return iam_client.get_role(RoleName=role_name)


def get_iam_role_arn(
        iam_client,
        role_name: str) -> str:
    """
    Gets ARN from IAM role by role name.
    """
    return iam_client.get_role(
        RoleName=role_name)['Role']['Arn']


def attach_policy_to_role(
        iam_client,
        role_name: str,
        policy_arn: str
) -> None:
    """
    Attaches policy to role.
    """
    iam_client.attach_role_policy(
        RoleName=role_name,
        PolicyArn=policy_arn
    )
