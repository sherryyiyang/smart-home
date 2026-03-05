import requests

base_url = "http://localhost:3000"
timeout = 30

def test_get_single_device_by_valid_id():
    # First, get all devices to find a valid existing device ID
    try:
        resp_devices = requests.get(f"{base_url}/devices", timeout=timeout)
        resp_devices.raise_for_status()
    except requests.RequestException as e:
        raise AssertionError(f"Failed to get devices list: {e}")
    devices = resp_devices.json()
    assert isinstance(devices, list) and len(devices) > 0, "Devices list is empty or invalid"

    device_id = devices[0].get("id")
    assert device_id is not None, "First device does not have an 'id' field"

    # Now, get the single device by id
    try:
        resp_device = requests.get(f"{base_url}/devices/{device_id}", timeout=timeout)
        resp_device.raise_for_status()
    except requests.RequestException as e:
        raise AssertionError(f"Failed to get device by id {device_id}: {e}")

    assert resp_device.status_code == 200, f"Unexpected status code: {resp_device.status_code}"
    device = resp_device.json()
    assert isinstance(device, dict), "Device response is not a JSON object"
    assert device.get("id") == device_id, "Returned device id does not match requested id"

test_get_single_device_by_valid_id()