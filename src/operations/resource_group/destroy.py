import requests
import logging

# Set logger
logger = logging.getLogger(__name__)


def delete_resource_group(
    subscription_id: str, resource_group_name: str, access_token: str
) -> bool:
    """
    This is a function to delete the resource group.
    :param susbcription_id: Azure subscription id
    :type susbcription_id: str
    :param resource_group_name: Azure resource group name
    :type resource_group_name: str
    :param access_token: Azure access token
    :type access_token: str
    :return: True if the resource group is deleted successfully, False otherwise
    :rtype: bool
    Example:
    >>> main(
            susbcription_id=d0a1b2c3-d4e5-f6g7-h8i9-j0k1l2m3n4o5,
            resource_group_name=example-rg,
            access_token=ey123xyz
            )
    True
    """
    url = f"https://management.azure.com/subscriptions/{subscription_id}/resourcegroups/{resource_group_name}?api-version=2020-06-01"

    payload = {}

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }

    try:
        response = requests.request("DELETE", url, headers=headers, data=payload)
        response.raise_for_status()
        if response.status_code == 202:
            logger.info(f"Resource group {resource_group_name} deleted successfully")
            return True
        else:
            logger.error(f"Resource group {resource_group_name} deletion failed")
            return False
    except requests.exceptions.HTTPError as err:
        logger.error(err)
        return False
    except Exception as err:
        logger.error(err)
        return False
