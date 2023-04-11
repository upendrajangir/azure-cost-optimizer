import requests
from typing import List, Dict


def get_resource_groups(
    subscription_id: str, access_token: str
) -> List[Dict[str, str]]:
    """
    Retrieves data for all resource groups in the specified subscription and returns it as a list of dictionaries.

    Args:
        subscription_id (str): The ID of the subscription to retrieve resource group data for.
        access_token (str): The access token to use for authentication.

    Raises:
        ValueError: If the subscription ID or access token is missing or invalid.
        Exception: If there is an error retrieving the data.

    Returns:
        List[Dict[str, str]]: A list of dictionaries containing the name, location, ID, type, and tags for each resource group.
    """
    # Validate input parameters
    if not subscription_id or not isinstance(subscription_id, str):
        raise ValueError("Subscription ID is missing or invalid")
    if not access_token or not isinstance(access_token, str):
        raise ValueError("Access token is missing or invalid")

    # Send request to Azure Management API to retrieve resource group data
    url = f"https://management.azure.com/subscriptions/{subscription_id}/resourcegroups?api-version=2020-06-01"
    headers = {"Authorization": f"Bearer {access_token}"}
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        raise Exception(f"Failed to retrieve resource groups data. Error: {e}")

    # Parse data from API response and create list of resource group dictionaries
    data = response.json()
    resource_groups = []
    for item in data.get("value", []):
        resource_group = {
            "name": item.get("name", ""),
            "location": item.get("location", ""),
            "id": item.get("id", ""),
            "type": item.get("type", ""),
            "tags": item.get("tags", {}),
        }
        resource_groups.append(resource_group)

    return resource_groups


def delete_resource_group(
    subscription_id: str, resource_group_name: str, access_token: str
) -> bool:
    """
    Deletes the specified resource group.

    Args:
        subscription_id (str): The ID of the subscription that the resource group belongs to.
        resource_group_name (str): The name of the resource group to delete.
        access_token (str): The access token to use for authentication.

    Raises:
        ValueError: If any of the required parameters are missing or invalid.
        Exception: If there is an error deleting the resource group.

    Returns:
        bool: True if the resource group was successfully deleted, False otherwise.
    """
    # Validate input parameters
    if not subscription_id or not isinstance(subscription_id, str):
        raise ValueError("Subscription ID is missing or invalid")
    if not resource_group_name or not isinstance(resource_group_name, str):
        raise ValueError("Resource group name is missing or invalid")
    if not access_token or not isinstance(access_token, str):
        raise ValueError("Access token is missing or invalid")

    # Check if the specified resource group exists and belongs to the specified subscription ID
    url = f"https://management.azure.com/subscriptions/{subscription_id}/resourcegroups/{resource_group_name}?api-version=2020-06-01"
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(url, headers=headers)
    if response.status_code == 404:
        print(
            f"Resource group {resource_group_name} not found in subscription {subscription_id}"
        )
        return False
    elif response.status_code != 200:
        raise Exception(f"Failed to check resource group. Error: {response.text}")

    # Send request to Azure Management API to delete resource group
    url = f"https://management.azure.com/subscriptions/{subscription_id}/resourcegroups/{resource_group_name}?api-version=2020-06-01"
    headers = {"Authorization": f"Bearer {access_token}"}
    try:
        response = requests.delete(url, headers=headers)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        raise Exception(f"Failed to delete resource group. Error: {e}")

    # Return True if the request was successful, False otherwise
    if response.status_code == 200:
        return True
    else:
        return False
