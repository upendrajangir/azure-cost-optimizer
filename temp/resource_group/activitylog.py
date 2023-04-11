from azure.identity import ClientSecretCredential
from azure.mgmt.monitor import MonitorManagementClient
from datetime import datetime, timedelta
import pytz

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


def get_monitor_client(tenant_id, client_id, client_secret, subscription_id):
    # Authenticate using the Service Principal credentials and create a MonitorManagementClient
    credential = ClientSecretCredential(
        tenant_id=tenant_id, client_id=client_id, client_secret=client_secret
    )
    return MonitorManagementClient(credential, subscription_id)


def list_resource_group_activity_logs(
    tenant_id,
    client_id,
    client_secret,
    subscription_id,
    resource_group_name,
    start_time=None,
):
    monitor_client = get_monitor_client(
        tenant_id, client_id, client_secret, subscription_id
    )

    if not start_time:
        start_time = datetime.now(pytz.UTC) - timedelta(days=90)

    # Create the filter string for querying activity logs
    filter_string = (
        f"eventTimestamp ge {start_time.isoformat()} and "
        f"resourceGroupName eq '{resource_group_name}'"
    )

    # Query the activity logs using the filter string
    activity_logs = monitor_client.activity_logs.list(filter=filter_string)

    return activity_logs


if __name__ == "__main__":

    tenant_id = (os.getenv("TENANT_ID"),)
    client_id = (os.getenv("CLIENT_ID"),)
    client_secret = (os.getenv("CLIENT_SECRET"),)
    subscription_id = "1400fdf5-6ba3-4b18-8541-647e95e73f10"
    resource_group_name = "test_rg"

    activity_logs = list_resource_group_activity_logs(
        "ea2b2786-e322-4ac3-ae45-a58d6989733f",
        "c30136c2-577f-4683-930e-18dc183d7293",
        "YHS8Q~pelO2kczmd4TLkoDXssB83BCathkGfHduh",
        "1400fdf5-6ba3-4b18-8541-647e95e73f10",
        "test_rg",
    )

    for log in activity_logs:
        print(
            f"Operation: {log.operation_name.value}, Timestamp: {log.event_timestamp}, Caller: {log.caller}"
        )
