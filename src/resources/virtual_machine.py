import requests


def get_azure_vm(
    subscription_id: str, resource_group_name: str, vm_name: str, access_token: str
) -> dict:
    """
    Gets information about an Azure VM.

    Args:
        subscription_id (str): The ID of the subscription that the resource group belongs to.
        resource_group_name (str): The name of the resource group that the VM belongs to.
        vm_name (str): The name of the VM to get information about.
        access_token (str): The access token to use for authentication.

    Raises:
        ValueError: If any of the required parameters are missing or invalid.
        Exception: If there is an error getting information about the VM.

    Returns:
        dict: Information about the VM in the form of a dictionary.
    """
    # Validate input parameters
    if not subscription_id or not isinstance(subscription_id, str):
        raise ValueError("Subscription ID is missing or invalid")
    if not resource_group_name or not isinstance(resource_group_name, str):
        raise ValueError("Resource group name is missing or invalid")
    if not vm_name or not isinstance(vm_name, str):
        raise ValueError("VM name is missing or invalid")
    if not access_token or not isinstance(access_token, str):
        raise ValueError("Access token is missing or invalid")

    # Send request to Azure Management API to get information about the VM
    url = f"https://management.azure.com/subscriptions/{subscription_id}/resourceGroups/{resource_group_name}/providers/Microsoft.Compute/virtualMachines/{vm_name}?api-version=2020-06-01"
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(url, headers=headers)
    if response.status_code == 404:
        raise Exception(
            f"VM {vm_name} not found in resource group {resource_group_name}"
        )
    elif response.status_code != 200:
        raise Exception(f"Failed to get VM information. Error: {response.text}")

    # Parse the response to get the VM information
    vm_info = response.json()
    return vm_info


def delete_azure_vm(
    subscription_id: str, resource_group_name: str, vm_name: str, access_token: str
) -> bool:
    """
    Deletes an Azure VM and all dependent resources.

    Args:
        subscription_id (str): The ID of the subscription that the resource group belongs to.
        resource_group_name (str): The name of the resource group that the VM belongs to.
        vm_name (str): The name of the VM to delete.
        access_token (str): The access token to use for authentication.

    Raises:
        ValueError: If any of the required parameters are missing or invalid.
        Exception: If there is an error deleting the VM or any dependent resources.

    Returns:
        bool: True if the VM and all dependent resources were successfully deleted, False otherwise.
    """
    # Validate input parameters
    if not subscription_id or not isinstance(subscription_id, str):
        raise ValueError("Subscription ID is missing or invalid")
    if not resource_group_name or not isinstance(resource_group_name, str):
        raise ValueError("Resource group name is missing or invalid")
    if not vm_name or not isinstance(vm_name, str):
        raise ValueError("VM name is missing or invalid")
    if not access_token or not isinstance(access_token, str):
        raise ValueError("Access token is missing or invalid")

    # Send request to Azure Management API to get information about the VM
    url = f"https://management.azure.com/subscriptions/{subscription_id}/resourceGroups/{resource_group_name}/providers/Microsoft.Compute/virtualMachines/{vm_name}?api-version=2020-06-01"
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(url, headers=headers)
    if response.status_code == 404:
        print(f"VM {vm_name} not found in resource group {resource_group_name}")
        return False
    elif response.status_code != 200:
        raise Exception(f"Failed to get VM information. Error: {response.text}")

    # Parse the response to get the IDs of any dependent resources (disks, NICs, public IPs)
    vm_info = response.json()
    nic_id = vm_info["properties"]["networkProfile"]["networkInterfaces"][0]["id"]
    disk_id = vm_info["properties"]["storageProfile"]["osDisk"]["managedDisk"]["id"]
    public_ip_id = (
        vm_info["properties"]["networkProfile"]["networkInterfaces"][0]["properties"][
            "ipConfigurations"
        ][0]
        .get("publicIpAddress", {})
        .get("id")
    )

    # Send request to Azure Management API to delete the VM
    url = f"https://management.azure.com/subscriptions/{subscription_id}/resourceGroups/{resource_group_name}/providers/Microsoft.Compute/virtualMachines/{vm_name}?api-version=2020-06-01"
    try:
        response = requests.delete(url, headers=headers)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        raise Exception(f"Failed to delete VM. Error: {e}")

    # Send request to Azure Management API to delete the dependent resources (disks, NICs, public IPs)

    # Delete the NIC
    url = f"https://management.azure.com/subscriptions/{subscription_id}/resourceGroups/{resource_group_name}/providers/Microsoft.Network/networkInterfaces/{nic_id}?api-version=2020-06-01"
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(url, headers=headers)
    if response.status_code == 404:
        print(f"NIC for {vm_name} is already deleted.")
        return False
    elif response.status_code != 200:
        raise Exception(f"Failed to get NIC information. Error: {response.text}")
    url = f"https://management.azure.com/subscriptions/{subscription_id}/resourceGroups/{resource_group_name}/providers/Microsoft.Network/networkInterfaces/{nic_id}?api-version=2020-06-01"
    try:
        response = requests.delete(url, headers=headers)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        raise Exception(f"Failed to delete NIC. Error: {e}")

    # Delete the Disk
    url = f"https://management.azure.com/subscriptions/{subscription_id}/resourceGroups/{resource_group_name}/providers/Microsoft.Compute/disks/{disk_id}?api-version=2020-06-01"
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(url, headers=headers)
    if response.status_code == 404:
        print(f"Disk for {vm_name} is already deleted.")
        return False
    elif response.status_code != 200:
        raise Exception(f"Failed to get Disk information. Error: {response.text}")
    url = f"https://management.azure.com/subscriptions/{subscription_id}/resourceGroups/{resource_group_name}/providers/Microsoft.Compute/disks/{disk_id}?api-version=2020-06-01"
    try:
        response = requests.delete(url, headers=headers)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        raise Exception(f"Failed to delete Disk. Error: {e}")

    # Delete the Public IP
    url = f"https://management.azure.com/subscriptions/{subscription_id}/resourceGroups/{resource_group_name}/providers/Microsoft.Network/publicIPAddresses/{public_ip_id}?api-version=2020-06-01"
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(url, headers=headers)
    if response.status_code == 404:
        print(f"Public IP for {vm_name} is already deleted.")
        return False
    elif response.status_code != 200:
        raise Exception(f"Failed to get Public IP information. Error: {response.text}")
    url = f"https://management.azure.com/subscriptions/{subscription_id}/resourceGroups/{resource_group_name}/providers/Microsoft.Network/publicIPAddresses/{public_ip_id}?api-version=2020-06-01"
    try:
        response = requests.delete(url, headers=headers)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        raise Exception(f"Failed to delete Public IP. Error: {e}")

    print(f"VM {vm_name} and dependent resources successfully deleted.")
    return True
