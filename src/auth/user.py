import adal
import logging

# Set logger
logger = logging.getLogger(__name__)


def get_token(tenant_id: str, email_id: str, password: str) -> str:
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
