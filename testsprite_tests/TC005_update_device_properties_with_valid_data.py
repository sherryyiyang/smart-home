import requests

BASE_URL = "http://localhost:3000"
TIMEOUT = 30

def test_update_device_properties_with_valid_data():
    # Fetch all devices
    resp = requests.get(f"{BASE_URL}/devices", timeout=TIMEOUT)
    assert resp.status_code == 200, f"Expected 200 from /devices, got {resp.status_code}"
    devices = resp.json()

    # Helper to find first device of a given type
    def find_device_by_type(dev_type):
        for d in devices:
            if d.get("type") == dev_type:
                return d
        return None

    # Define update payloads per device type
    updates = {
        "Light": {"on": True},
        "Thermostat": {"temperature": 72},
        "Lock": {"locked": True}
    }

    for device_type, update_body in updates.items():
        device = find_device_by_type(device_type)
        assert device is not None, f"No device found of type {device_type}"
        device_id = device["id"]

        try:
            patch_resp = requests.patch(f"{BASE_URL}/devices/{device_id}", json=update_body, timeout=TIMEOUT)
            assert patch_resp.status_code == 200, f"PATCH /devices/{device_id} returned {patch_resp.status_code}, expected 200"
            updated_device = patch_resp.json()

            # Verify updated fields present and correct
            for key, val in update_body.items():
                assert key in updated_device, f"Field '{key}' not in updated device response"
                assert updated_device[key] == val, f"Field '{key}' value {updated_device[key]} does not match update {val}"

            # Also verify the returned device id matches request id
            assert updated_device.get("id") == device_id, "Updated device id mismatch"

        except requests.RequestException as e:
            assert False, f"Request exception occurred: {e}"

test_update_device_properties_with_valid_data()