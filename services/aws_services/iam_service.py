import json


def get_doc_provide_access_lambda():
    document = {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Action": [
                    "sts:AssumeRole"
                ],
                "Principal": {
                    "Service": [
                        "lambda.amazonaws.com"
                    ]
                }
            }
        ]
    }
    return json.dumps(document)


def get_policy_json():
    policy_json = {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Action": [
                    "s3:*",
                    "s3-object-lambda:*",
                ],
                "Resource": "*"
            }
        ]
    }
    return json.dumps(policy_json)


def create_policy_for_role(iam_client, policy_name, policy_document):
    return iam_client.create_policy(
        PolicyName=policy_name,
        PolicyDocument=policy_document
    )


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


def get_list_policies(iam_client):
    return iam_client.list_policies()

