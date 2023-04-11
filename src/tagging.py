from azure.identity import ClientSecretCredential
from azure.mgmt.monitor import MonitorManagementClient
from datetime import datetime, timedelta
import requests
import json
import logging
from typing import Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

logging.basicConfig(level=logging.INFO)


def is_valid_email(email: str) -> bool:
    if "@" not in email:
        return False
    return True


def fetch_resource_group_creator_email(
    subscription_id: str, resource_group_name: str, access_token: str
) -> Optional[str]:
    """
    Fetch the email ID of the user who created a resource group in Azure.

    :param subscription_id: Azure subscription ID.
    :param resource_group_name: Name of the resource group.
    :param access_token: Azure access token.
    :return: Email ID of the user who created the resource group, or None if not found.
    """

    # Validate input parameters
    if not subscription_id:
        logging.error("Invalid input: subscription_id is required.")
        return None
    if not resource_group_name:
        logging.error("Invalid input: resource_group_name is required.")
        return None
    if not access_token:
        logging.error("Invalid input: access_token is required.")
        return None

    # Set time range for activity log query (e.g., last 30 days)
    end_time = datetime.utcnow()
    start_time = end_time - timedelta(days=7)
    start_time_str = start_time.strftime("%Y-%m-%dT%H:%M:%SZ")
    end_time_str = end_time.strftime("%Y-%m-%dT%H:%M:%SZ")

    # Construct the activity logs URL
    url = (
        f"https://management.azure.com/subscriptions/{subscription_id}/providers/microsoft.insights/eventtypes/management/values"
        f"?api-version=2017-03-01-preview&$filter=eventTimestamp ge '{start_time_str}' and eventTimestamp le '{end_time_str}'"
        f" and resourceGroupName eq '{resource_group_name}' and operationName eq 'Microsoft.Resources/subscriptions/resourcegroups/write'"
    )
    headers = {"Authorization": f"Bearer {access_token}"}

    try:
        # Fetch the activity logs
        response = requests.get(url, headers=headers)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        logging.error(f"Error fetching activity logs: {e}")
        return None

    try:
        # Parse the JSON response
        response_data = response.json()
    except json.JSONDecodeError as e:
        logging.error(f"Error decoding response JSON: {e}")
        return None

    if not response_data or not response_data.get("value"):
        logging.warning("No matching activity logs found.")
        return None

    # Extract the email ID of the user who created the resource
    creator_email = None
    for log_entry in response_data["value"]:
        if "caller" in log_entry:
            creator_email = log_entry["caller"]
            break

    if creator_email is None:
        logging.warning("Resource group creator email not found.")
    elif not is_valid_email(creator_email):
        logging.error(f"Invalid email format: {creator_email}")
        creator_email = None

    return creator_email


def add_owner_email_tag(
    subscription_id: str, resource_group_name: str, owner_email: str, access_token: str
) -> bool:
    """
    Add an "OwnerEmail" tag to a resource group in Azure.

    :param subscription_id: Azure subscription ID.
    :param resource_group_name: Name of the resource group.
    :param owner_email: Email ID of the owner.
    :param access_token: Azure access token.
    :return: True if the tag was added successfully, False otherwise.
    """

    # Validate input parameters
    if not subscription_id:
        logging.error("Invalid input: subscription_id is required.")
        return False
    if not resource_group_name:
        logging.error("Invalid input: resource_group_name is required.")
        return False
    if not owner_email:
        logging.error("Invalid input: owner_email is required.")
        return False
    if not access_token:
        logging.error("Invalid input: access_token is required.")
        return False

    # Fetch the existing tags for the resource group
    url = f"https://management.azure.com/subscriptions/{subscription_id}/resourcegroups/{resource_group_name}?api-version=2021-04-01"
    headers = {"Authorization": f"Bearer {access_token}"}
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        logging.error(f"Error fetching resource group: {e}")
        return False

    resource_group_data = response.json()
    tags = resource_group_data.get("tags", {})

    # Add the "OwnerEmail" tag to the resource group
    tags["OwnerEmail"] = owner_email

    # Update the resource group with the new tags
    payload = {"tags": tags}
    try:
        response = requests.patch(url, headers=headers, json=payload)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        logging.error(f"Error updating resource group tags: {e}")
        return False

    logging.info(
        f"Successfully added OwnerEmail tag to resource group {resource_group_name}."
    )
    return True


def add_ttl_tag(
    subscription_id: str, resource_group_name: str, ttl_value: int, access_token: str
) -> bool:
    """
    Add a "TTL" tag to a resource group in Azure.

    :param subscription_id: Azure subscription ID.
    :param resource_group_name: Name of the resource group.
    :param ttl_value: Time to live value (in days).
    :param access_token: Azure access token.
    :return: True if the tag was added successfully, False otherwise.
    """
    # Validate input parameters
    if not subscription_id:
        logging.error("Invalid input: subscription_id is required.")
        return False
    if not resource_group_name:
        logging.error("Invalid input: resource_group_name is required.")
        return False
    if ttl_value < 1:
        logging.error("Invalid input: ttl_value must be greater than or equal to 1.")
        return False
    if not access_token:
        logging.error("Invalid input: access_token is required.")
        return False

    # Fetch the existing tags for the resource group
    url = f"https://management.azure.com/subscriptions/{subscription_id}/resourcegroups/{resource_group_name}?api-version=2021-04-01"
    headers = {"Authorization": f"Bearer {access_token}"}
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        logging.error(f"Error fetching resource group: {e}")
        return False

    resource_group_data = response.json()
    tags = resource_group_data.get("tags", {})

    # Add the "TTL" tag to the resource group
    tags["TTL"] = str(ttl_value)

    # Update the resource group with the new tags
    payload = {"tags": tags}
    try:
        response = requests.patch(url, headers=headers, json=payload)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        logging.error(f"Error updating resource group tags: {e}")
        return False

    logging.info(f"Successfully added TTL tag to resource group {resource_group_name}.")
    return True
