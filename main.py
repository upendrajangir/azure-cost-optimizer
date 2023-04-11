# Imports: pypi libraries
import os
from dotenv import load_dotenv
import coloredlogs
import logging

# Imports: modules
from src.auth import get_access_token_service_principal
from src.tagging import (
    check_resource_group_owner_email_tag,
    add_owner_email_tag,
    check_resource_group_ttl_tag,
    add_ttl_tag,
    fetch_resource_group_creator_email,
)
from resources.resource_group import get_resource_groups

# Load environment variables
load_dotenv()

# Set logging
logger = logging.getLogger(__name__)
coloredlogs.install(
    fmt="%(asctime)s | %(hostname)s | %(levelname)s | %(name)s | %(filename)s:%(lineno)d | %(message)s",
    level="DEBUG",
)


def main(
    tenant_id: str, client_id: str, client_secret: str, subscription_id: str
) -> bool:
    """
    This is the main function of project that takes an azure app credentials and perform the actions defined.

    :param tenant_id: Azure tenant id
    :type tenant_id: str
    :param client_id: Azure app client id
    :type client_id: str
    :param client_secret: Azure app client secret
    :type client_secret: str
    :return: Status of the operation
    :rtype: bool

    Example:
    >>> main(
            tenant_id=d0a1b2c3-d4e5-f6g7-h8i9-j0k1l2m3n4o5,
            client_id=d0a1b2c3-d4e5-f6g7-h8i9-j0k1l2m3n4o5,
            client_secret=d0a1b2c3-d4e5-f6g7-h8i9-j0k1l2m3n4o5
            )
    True
    """
    # Get access token
    access_token = get_access_token_service_principal(
        tenant_id=tenant_id, client_id=client_id, client_secret=client_secret
    )

    # Fetch resource groups list
    resource_groups = get_resource_groups(
        subscription_id=subscription_id, access_token=access_token
    )

    # Tag resource groups
    for resource_group in resource_groups:
        logger.info(f"Tagging resource group: {resource_group['name']}")
        owner_email_id = fetch_resource_group_creator_email(
            subscription_id=subscription_id,
            resource_group_name=resource_group["name"],
            access_token=access_token,
        )
        # Check if owner email tag is present
        if not check_resource_group_owner_email_tag(
            subscription_id=subscription_id,
            resource_group_name=resource_group["name"],
            access_token=access_token,
        ):
            add_owner_email_tag(
                subscription_id=subscription_id,
                resource_group_name=resource_group["name"],
                owner_email=owner_email_id,
                access_token=access_token,
            )
        # Check if ttl tag is present
        if not check_resource_group_ttl_tag(
            subscription_id=subscription_id,
            resource_group_name=resource_group["name"],
            access_token=access_token,
        ):
            add_ttl_tag(
                subscription_id=subscription_id,
                resource_group_name=resource_group["name"],
                ttl_value="7",
                access_token=access_token,
            )

    return True


if __name__ == "__main__":
    main(
        tenant_id=os.getenv("TENANT_ID"),
        client_id=os.getenv("CLIENT_ID"),
        client_secret=os.getenv("CLIENT_SECRET"),
    )
