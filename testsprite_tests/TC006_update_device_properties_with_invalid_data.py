import requests

BASE_URL = "http://localhost:3000"
TIMEOUT = 30


def test_update_device_properties_with_invalid_data():
    # Step 1: Get list of devices to find a Light device ID
    try:
        resp_devices = requests.get(f"{BASE_URL}/devices", timeout=TIMEOUT)
        resp_devices.raise_for_status()
        devices = resp_devices.json()
        assert isinstance(devices, list) and len(devices) > 0, "Devices list is empty or invalid"
        # Find a Light device
        light_device = None
        for device in devices:
            if device.get("type") == "Light":
                light_device = device
                break
        assert light_device is not None, "No Light device found in device list"
        device_id = light_device.get("id")
        assert device_id, "Device ID not found in Light device list"
    except Exception as e:
        raise AssertionError(f"Failed to get devices or extract valid Light device ID: {e}")

    # Step 2: Attempt to PATCH device with invalid brightness type
    invalid_payload = {"brightness": "high"}
    try:
        resp_patch = requests.patch(f"{BASE_URL}/devices/{device_id}", json=invalid_payload, timeout=TIMEOUT)
    except requests.RequestException as e:
        raise AssertionError(f"PATCH request failed: {e}")

    # Step 3: Assert 400 Bad Request and proper error message
    assert resp_patch.status_code == 400, f"Expected 400 status code, got {resp_patch.status_code}"

    # Response should be JSON containing an error message indicating invalid fields
    try:
        error_response = resp_patch.json()
    except Exception:
        raise AssertionError("Response is not valid JSON")

    # We expect an 'Invalid fields' error message somewhere in the response
    error_messages = []
    if isinstance(error_response, dict):
        for v in error_response.values():
            if isinstance(v, str):
                error_messages.append(v.lower())
            elif isinstance(v, list):
                error_messages.extend([str(item).lower() for item in v])
    error_messages_text = " ".join(error_messages)
    assert "invalid fields" in error_messages_text, f"Expected 'Invalid fields' error message, got: {error_response}"


test_update_device_properties_with_invalid_data()
