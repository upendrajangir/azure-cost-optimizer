import requests
import datetime
import logging

# Set logger
logger = logging.getLogger(__name__)

timestamp = (datetime.datetime.today() - datetime.timedelta(days=89)).strftime(
    "%Y-%m-%dT%H:%M:%S.%fZ"
)


def get_resource_group_owner(
    subscription_id: str, resource_group_name: str, access_token: str
) -> str:
    """
    This is a function to get the owner (email id) of the resource group.

    :param susbcription_id: Azure subscription id
    :type susbcription_id: str
    :param resource_group_name: Azure resource group name
    :type resource_group_name: str
    :param access_token: Azure access token
    :type access_token: str
    :return: Email Id of the owner of the resource group
    :rtype: str

    Example:
    >>> main(
            susbcription_id=d0a1b2c3-d4e5-f6g7-h8i9-j0k1l2m3n4o5,
            resource_group_name=example-rg,
            access_token=ey123xyz
            )
    exampleuser@demoad.com
    """
    rg_creation_operation_name = (
        "Microsoft.Resources/subscriptions/resourceGroups/write"
    )
    rg_creation_status_code = "Created"
    get_event_api = f"https://management.azure.com/subscriptions/{subscription_id}/providers/Microsoft.Insights/eventtypes/management/values?api-version=2015-04-01&$select=operationName,caller,properties,resourceGroupName&$filter=eventTimestamp ge '{timestamp}' "
    event_payload = {}
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }
    try: # Try to get the owner of the resource group
        response = requests.request(
            "GET", get_event_api, headers=headers, data=event_payload
        )
        for data in response.json().get("value"):
            if (
                data.get("operationName").get("value") == rg_creation_operation_name
                and data.get("properties").get("statusCode") == rg_creation_status_code
                and data.get("resourceGroupName") == resource_group_name
            ):
                return data.get("caller")
    except requests.exceptions.HTTPError as err:
        logger.error(err)
        return None
    except Exception as err:
        logger.error(err)
        return None

