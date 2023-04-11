import requests
import logging
from datetime import datetime, timedelta
from typing import Optional, Dict, List
from ..send_email import send_email


def fetch_vm_consumption_data(
    subscription_id: str, resource_group_name: str, vm_name: str, access_token: str
) -> Optional[Dict]:
    """
    Fetch consumption data for a virtual machine (VM) in Azure, including CPU usage, memory usage, storage IOPS, and network data.

    :param subscription_id: Azure subscription ID.
    :param resource_group_name: Name of the resource group containing the VM.
    :param vm_name: Name of the virtual machine.
    :param access_token: Azure access token.
    :return: Dictionary with consumption data, or None if an error occurred.
    """
    # Validate input parameters
    if not subscription_id:
        logging.error("Invalid input: subscription_id is required.")
        return None
    if not resource_group_name:
        logging.error("Invalid input: resource_group_name is required.")
        return None
    if not vm_name:
        logging.error("Invalid input: vm_name is required.")
        return None
    if not access_token:
        logging.error("Invalid input: access_token is required.")
        return None

    # Set time range for metric query (e.g., last 7 days)
    end_time = datetime.utcnow()
    start_time = end_time - timedelta(days=7)
    start_time_str = start_time.strftime("%Y-%m-%dT%H:%M:%SZ")
    end_time_str = end_time.strftime("%Y-%m-%dT%H:%M:%SZ")

    # Metric names and aggregation types to fetch
    metrics = [
        ("Percentage CPU", "Average"),
        ("Available Memory Bytes", "Average"),
        ("Data Disk Read Bytes/sec", "Average"),
        ("Data Disk Write Bytes/sec", "Average"),
        ("Network In Total", "Total"),
        ("Network Out Total", "Total"),
    ]

    consumption_data = {}

    for metric_name, aggregation_type in metrics:
        url = f"https://management.azure.com/subscriptions/{subscription_id}/resourceGroups/{resource_group_name}/providers/Microsoft.Compute/virtualMachines/{vm_name}/providers/microsoft.insights/metrics?api-version=2018-01-01&metricnames={metric_name}&aggregation={aggregation_type}&startTime={start_time_str}&endTime={end_time_str}"
        headers = {"Authorization": f"Bearer {access_token}"}
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            logging.error(f"Error fetching VM metrics for {metric_name}: {e}")
            return None

        metrics_data = response.json()

        if metrics_data and metrics_data.get("value"):
            metric = metrics_data["value"][0]
            if metric["timeseries"] and metric["timeseries"][0]["data"]:
                data_points = metric["timeseries"][0]["data"]
                if aggregation_type == "Average":
                    total_value = sum(
                        [
                            data_point["average"]
                            for data_point in data_points
                            if data_point["average"] is not None
                        ]
                    )
                    average_value = total_value / len(data_points)
                    consumption_data[metric_name] = average_value
                elif aggregation_type == "Total":
                    total_value = sum(
                        [
                            data_point["total"]
                            for data_point in data_points
                            if data_point["total"] is not None
                        ]
                    )
                    consumption_data[metric_name] = total_value

    return consumption_data


def analyze_vm_consumption_data(consumption_data: Dict) -> Optional[str]:
    """
    Analyze consumption data of a resource and suggest a better fit resource SKU.

    :param consumption_data: Dictionary containing resource consumption data.
    :return: Suggested resource SKU, or None if no suggestion can be made.
    """
    # Check input data
    if not consumption_data:
        return None

    # Analyze consumption data
    # TODO: Implement specific logic for analyzing consumption data and suggesting a better fit resource SKU.

    # Example:
    # if resource_type == "virtual_machine":
    #     if average_cpu_usage < threshold:
    #         return "d2sv3"
    #     elif ...

    suggested_sku = None

    return suggested_sku


def send_recommendation_email(
    subscription_id: str,
    resource_group_name: str,
    access_token: str,
    from_email: str,
    to_email: List[str],
    recommendation_data: Dict[str, str],
) -> None:
    """
    Sends a recommendation email to the specified user.

    Args:
        subscription_id (str): The subscription ID.
        resource_group_name (str): The name of the resource group.
        access_token (str): The access token to use for authentication.
        from_email (str): The email address to use as the sender.
        to_email (List[str]): A list of email addresses to send the email to.
        recommendation_data (Dict[str, str]): The recommendation data, including the name of the resource, current and recommended sizes, and usage data.

    Raises:
        ValueError: If any of the required parameters are missing or invalid.
        Exception: If there is an error sending the email.
    """

    # Validate input parameters
    if not subscription_id:
        raise ValueError("Subscription ID is missing or invalid")
    if not resource_group_name:
        raise ValueError("Resource group name is missing or invalid")
    if not access_token:
        raise ValueError("Access token is missing or invalid")
    if not from_email:
        raise ValueError("Sender email is missing or invalid")
    if not to_email or not all([email.strip() for email in to_email]):
        raise ValueError("Recipient email(s) is missing or invalid")
    if not recommendation_data or not isinstance(recommendation_data, dict):
        raise ValueError("Recommendation data is missing or invalid")

    # Get the resource name and type from the recommendation data
    virtual_machine_name = recommendation_data.get("name")
    current_size = recommendation_data.get("current_size")
    cpu_utilization = recommendation_data.get("cpu_utilization")
    memory_utilization = recommendation_data.get("memory_utilization")
    storage_utilization = recommendation_data.get("storage_utilization")
    network_utilization = recommendation_data.get("network_utilization")
    new_size = recommendation_data.get("new_size")

    # Send the email using the template
    is_html = (True,)
    subject = f"Resource Optimization Suggestion | {virtual_machine_name}"
    template = f""" 
        Dear User,

        Based on our analysis of your resource usage, we've identified that the virtual machine you're currently using is overpowered for your use case. We suggest that you consider changing the VM size to optimize your resource usage.

        The current VM size is: {current_size}.
        The average CPU utilization over the past week was: {cpu_utilization}%.
        The average memory utilization over the past week was: {memory_utilization}%.
        The average storage IOPS over the past week was: {storage_utilization}.
        The average network throughput over the past week was: {network_utilization}.
        Based on these metrics, we suggest that you change the VM size to {new_size}, which is a more appropriate size for your use case.

        Please note that if you don't take any action within the next 3 days, we'll forcefully change the VM size to the suggested size to optimize your resource usage and reduce costs.

        Thank you for your attention to this matter.

        Best regards,
        Resource Optimization Team
    """

    msg = template

    send_email(subject, msg, from_email, to_email, is_html=is_html)
