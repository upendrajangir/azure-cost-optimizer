# Imports: pypi libraries
import os
import requests
from dotenv import load_dotenv
import coloredlogs
import logging


# Imports: modules
from auth.app import get_token

# Load environment variables
load_dotenv()

# Set logging
logger = logging.getLogger(__name__)
coloredlogs.install(
    fmt="%(asctime)s | %(hostname)s | %(levelname)s | %(name)s | %(filename)s:%(lineno)d | %(message)s",
    level="DEBUG",
)


def main(tenant_id: str, client_id: str, client_secret: str) -> bool:
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
    return True


if __name__ == "__main__":
    main(
        tenant_id=os.getenv("TENANT_ID"),
        client_id=os.getenv("CLIENT_ID"),
        client_secret=os.getenv("CLIENT_SECRET"),
    )
