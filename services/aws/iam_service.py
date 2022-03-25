
def create_iam_role(iam_client, role_name, role_policy_document):
    iam_client.create_role(
        RoleName=role_name,
        AssumeRolePolicyDocument=role_policy_document,
    )


def get_iam_role(iam_client, role_name):
    return iam_client.get_role(RoleName=role_name)


def get_iam_role_arn(iam_client, role_name):
    return iam_client.get_role(
        RoleName=role_name)['Role']['Arn']


def attach_policy_to_role(iam_client, role_name, policy_arn):
    iam_client.attach_role_policy(
        RoleName=role_name,
        PolicyArn=policy_arn
    )
