import requests
import datetime
import json
import logging

# Set logger
logger = logging.getLogger(__name__)

# Set timestamp variable
timestamp = (datetime.datetime.today() - datetime.timedelta(days=89)).strftime(
    "%Y-%m-%dT%H:%M:%S.%fZ"
)


def get_tags():
    pass


def add_owner_email_tag(
    subscription_id: str,
    resource_group_name: str,
    owner_email_id: str,
    access_token: str,
) -> bool:
    """
    This is a function to update the owner (email id) of the resource group as tag CreatedBy.

    :param susbcription_id: Azure subscription id
    :type susbcription_id: str
    :param resource_group_name: Azure resource group name
    :type resource_group_name: str
    :param owner_email_id: Email Id of the owner of the resource group
    :type owner_email_id: str
    :param access_token: Azure access token
    :type access_token: str
    :return: Email Id of the owner of the resource group
    :rtype: str

    Example:
    >>> main(
            susbcription_id=d0a1b2c3-d4e5-f6g7-h8i9-j0k1l2m3n4o5,
            resource_group_name=example-rg,
            owner_email_id=example@examplead.com,
            access_token=ey123xyz
            )
    true
    """
    update_tag_api = f"https://management.azure.com/subscriptions/{subscription_id}/resourcegroups/{resource_group_name}/providers/Microsoft.Resources/tags/default?api-version=2021-04-01"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }
    updated_tag_payload = json.dumps(
        {
            "operation": "merge",
            "properties": {"tags": {"CreatedBy": f"{owner_email_id}"}},
        }
    )
    try:
        response = requests.request(
            "PATCH", update_tag_api, headers=headers, data=updated_tag_payload
        )
        response.raise_for_status()
        logging.info("owner tag added successfully")
        return True
    except requests.exceptions.HTTPError as err:
        logger.error(err)
        return False
    except Exception as err:
        logger.error(err)
        return False


def delete_tag():
    pass


def update_tag():
    pass
