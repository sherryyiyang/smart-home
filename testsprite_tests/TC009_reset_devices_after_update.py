import requests

BASE_URL = "http://localhost:3000"
TIMEOUT = 30

def test_reset_devices_after_update():
    session = requests.Session()
    try:
        # Step 1: Get devices to find one device to update
        resp = session.get(f"{BASE_URL}/devices", timeout=TIMEOUT)
        assert resp.status_code == 200, f"Expected 200, got {resp.status_code}"
        devices = resp.json()
        assert isinstance(devices, list) and len(devices) > 0, "Devices list is empty or not a list"

        device = devices[0]
        device_id = device.get("id")
        assert device_id, "Device ID not found"

        # Save default device state for comparison after reset
        default_device = next((d for d in devices if d.get("id") == device_id), None)
        assert default_device is not None, "Default device not found"

        # Determine a valid patch payload depending on device type present fields
        patch_payload = None
        # A Light device might have "on" and "brightness"
        if "on" in device and isinstance(device["on"], bool):
            # Toggle the 'on' state
            patch_payload = {"on": not device["on"]}
        elif "temperature" in device and isinstance(device["temperature"], (int, float)):
            # Change temperature to a different value
            new_temp = device["temperature"] + 1 if device["temperature"] < 100 else device["temperature"] - 1
            patch_payload = {"temperature": new_temp}
        elif "locked" in device and isinstance(device["locked"], bool):
            patch_payload = {"locked": not device["locked"]}
        else:
            # If no recognized props, just try {"on": true} as a fallback
            patch_payload = {"on": True}

        # Step 2: PATCH /devices/:id with valid update
        patch_resp = session.patch(
            f"{BASE_URL}/devices/{device_id}",
            json=patch_payload,
            timeout=TIMEOUT
        )
        assert patch_resp.status_code == 200, f"PATCH expected 200, got {patch_resp.status_code}"
        updated_device = patch_resp.json()
        # Assert that the updated fields match request
        for key, val in patch_payload.items():
            assert updated_device.get(key) == val, f"Expected {key}={val} in updated device"

        # Step 3: POST /reset to reset all devices
        reset_resp = session.post(f"{BASE_URL}/reset", timeout=TIMEOUT)
        assert reset_resp.status_code == 200, f"Reset expected 200, got {reset_resp.status_code}"
        reset_json = reset_resp.json()
        assert "message" in reset_json and isinstance(reset_json["message"], str) and len(reset_json["message"]) > 0

        # Step 4: GET /devices to verify devices reset to default states
        post_reset_resp = session.get(f"{BASE_URL}/devices", timeout=TIMEOUT)
        assert post_reset_resp.status_code == 200, f"Post-reset GET devices expected 200, got {post_reset_resp.status_code}"
        post_reset_devices = post_reset_resp.json()
        assert isinstance(post_reset_devices, list) and len(post_reset_devices) > 0

        # Check device with same ID matches default state (not patched)
        post_reset_device = next((d for d in post_reset_devices if d.get("id") == device_id), None)
        assert post_reset_device is not None, "Reset device not found in device list"

        # Verify the reset device properties match the default device properties for the patched keys
        for key in patch_payload.keys():
            assert post_reset_device.get(key) == default_device.get(key), f"Device property {key} was not reset to default"

    finally:
        session.close()

test_reset_devices_after_update()