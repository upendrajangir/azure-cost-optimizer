from azure.mgmt.monitor import MonitorManagementClient
from datetime import datetime, timedelta
import pytz

import os
from dotenv import load_dotenv
from azure.identity import ClientSecretCredential

# Load environment variables
load_dotenv()



def get_monitor_client(subscription_id, credential):
    return MonitorManagementClient(credential, subscription_id)

def find_resource_group_owner(subscription_id, resource_group_name,credential, start_time=None):
    # Get an instance of MonitorManagementClient
    monitor_client = get_monitor_client(subscription_id, credential)

    # Set the start_time to 90 days ago if not provided
    if not start_time:
        start_time = datetime.now(pytz.UTC) - timedelta(days=90)

    # Create the filter string for querying activity logs
    filter_string = (
        f"eventTimestamp ge {start_time.isoformat()} and "
        f"resourceGroupName eq '{resource_group_name}' "
    )

    # Query the activity logs using the filter string
    activity_logs = monitor_client.activity_logs.list(filter=filter_string)

    for logs in activity_logs:
        print(logs)
    # Iterate through the logs to find the 'caller' property, which indicates the owner
    for log in activity_logs:
        if 'caller' in log.properties:
            return log.properties['caller']

    # Return None if no owner is found
    return None

if __name__ == "__main__":
    subscription_id = "1400fdf5-6ba3-4b18-8541-647e95e73f10",
    resource_group_name = "test_rg",

    credential = ClientSecretCredential(
        tenant_id=os.getenv("AZURE_TENANT_ID"),
        client_id=os.getenv("AZURE_CLIENT_ID"),
        client_secret=os.getenv("AZURE_CLIENT_SECRET"),
    )
    
    # Call find_resource_group_owner to get the owner of the specified resource group
    owner = find_resource_group_owner(subscription_id, resource_group_name, credential=credential)

    # Print the owner if found, otherwise print a message indicating the owner was not found
    if owner:
        print(f"The owner of the resource group '{resource_group_name}' is: {owner}")
    else:
        print("Could not find the owner of the resource group.")
