
import logging
from typing import Sequence

from botocore.exceptions import ClientError

from services.aws.iam_service import (
    create_iam_role,
    attach_policy_to_role,
)
from services.aws.values import get_doc_provide_access_lambda


logger = logging.getLogger(__name__)


def create_role_and_policy(
        iam_client,
        role_name: str,
        arn_policies: Sequence[str]
) -> None:
    """
    Creates role with kit of default policies from AWS.
    """
    role_policy_document = get_doc_provide_access_lambda()
    try:
        create_iam_role(
            iam_client=iam_client,
            role_name=role_name,
            role_policy_document=role_policy_document
        )
    except Exception:
        logger.exception(
            f'Could not create a role with name {role_name}')
        raise
    for policy_arn in arn_policies:
        try:
            attach_policy_to_role(
                iam_client=iam_client,
                role_name=role_name,
                policy_arn=policy_arn
            )
        except ClientError:
            logger.exception(
                (f'Could not attach policy "{policy_arn}"'
                 f'to role "{role_name}"')
            )
            raise
