# Imports: pypi libraries
import requests
import logging
import adal

# Set logger
logger = logging.getLogger(__name__)


def get_access_token_service_principal(
    tenant_id: str, client_id: str, client_secret: str
) -> str:
    """
    This function gets an access token from Azure AD.

    :param tenant_id: Azure tenant id
    :type tenant_id: str
    :param client_id: Azure app client id0p;
    :type client_id: str
    :param client_secret: Azure app client secret
    :type client_secret: str
    :return: Access token
    :rtype: str
    """
    url = f"https://login.microsoftonline.com/{tenant_id}/oauth2/token"
    data = {
        "grant_type": "client_credentials",
        "client_id": client_id,
        "client_secret": client_secret,
        "resource": "https://management.azure.com/",
    }

    try:
        response = requests.post(url, data=data)
        response.raise_for_status()
        access_token = response.json()["access_token"]
        logger.info("Successfully retrieved access token")
        return access_token
    except requests.exceptions.HTTPError as err:
        logger.error(f"HTTP error occurred: {err}")
        return None
    except requests.exceptions.ConnectionError as err:
        logger.error(f"Error Connecting: {err}")
        return None
    except requests.exceptions.Timeout as err:
        logger.error(f"Timeout Error: {err}")
        return None
    except requests.exceptions.RequestException as err:
        logger.error(f"Something went wrong: {err}")
        return None


def get_access_token_user_credentials(
    tenant_id: str, email_id: str, password: str
) -> str:
    """
    This function gets an access token from Azure AD.

    :param tenant_id: Azure tenant id
    :type tenant_id: str
    :param client_id: Azure user client id
    :type client_id: str
    :param email_id: Azure user email
    :type email_id: str
    :param password: Azure user password
    :type password: str
    :return: Access token
    :rtype: str
    """
    # Set the resource URL
    resource = "https://management.azure.com/"

    # Get an authentication context
    context = adal.AuthenticationContext(
        f"https://login.microsoftonline.com/{tenant_id}"
    )

    try:
        # Acquire an access token
        access_token = context.acquire_token_with_username_password(
            resource, email_id, password
        )
        logger.info("Successfully retrieved access token")
        return access_token
    except adal.adal_error.AdalError as err:
        logger.error(f"Error occurred: {err}")
        return None
    except Exception as err:
        logger.error(f"Something went wrong: {err}")
        return None
