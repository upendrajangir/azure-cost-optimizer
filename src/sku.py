import requests
from typing import List, Dict


def get_vm_skus(subscription_id: str, location: str, access_token: str):
    """
    Retrieves the available VM skus for the specified location.

    Args:
        location (str): The Azure region for which to retrieve VM skus.
        access_token (str): The access token to use for authentication.

    Returns:
        dict: A dictionary containing information about the available VM skus.
    """
    # Validate input parameters
    if not location or not isinstance(location, str):
        raise ValueError("Location is missing or invalid")
    if not access_token or not isinstance(access_token, str):
        raise ValueError("Access token is missing or invalid")

    # Construct the URL for the request
    url = f"https://management.azure.com/subscriptions/{subscription_id}/providers/Microsoft.Compute/skus?api-version=2021-07-01&$filter=location eq '{location}'"

    # Set up the request headers
    headers = {"Authorization": f"Bearer {access_token}"}

    # Send the request to the Azure Management API
    response = requests.get(url, headers=headers)

    # Check the response status code and return the result
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Failed to retrieve VM skus. Error: {response.text}")


def add_vm_skus_to_db(vm_skus: List[Dict], session: Session) -> bool:
    """
    Adds the given list of VM SKU data to the SQLite database table using the provided SQLAlchemy session.

    Args:
        vm_skus (List[Dict]): List of VM SKU data, each represented as a dictionary.
        session (Session): SQLAlchemy session object to use for database operations.

    Returns:
        None
    """
    # TODO: Implement logic to add VM SKU data to the database
    return True
