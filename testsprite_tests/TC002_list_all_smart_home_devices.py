import requests

BASE_URL = "http://localhost:3000"
TIMEOUT = 30

def test_list_all_smart_home_devices():
    url = f"{BASE_URL}/devices"
    try:
        response = requests.get(url, timeout=TIMEOUT)
        response.raise_for_status()
    except requests.RequestException as e:
        assert False, f"Request to {url} failed: {e}"

    assert response.status_code == 200, f"Expected status code 200 but got {response.status_code}"
    
    try:
        devices = response.json()
    except ValueError:
        assert False, "Response is not valid JSON"

    assert isinstance(devices, list), "Response JSON is not a list"
    device_types = {"Light": False, "Thermostat": False, "Lock": False}

    # Check each device has required keys and types and mark types found
    for device in devices:
        assert isinstance(device, dict), "Each device should be a JSON object"
        assert "type" in device, "Device missing 'type' field"
        dtype = device["type"]
        assert dtype in device_types, f"Unexpected device type '{dtype}'"
        device_types[dtype] = True

        # Validate current states depending on type
        if dtype == "Light":
            assert "on" in device and isinstance(device["on"], bool), "'Light' device missing boolean 'on' state"
            assert "brightness" in device and isinstance(device["brightness"], (int, float)), "'Light' device missing numeric 'brightness'"
        elif dtype == "Thermostat":
            assert "on" in device and isinstance(device["on"], bool), "'Thermostat' device missing boolean 'on' state"
            assert "temperature" in device and isinstance(device["temperature"], (int, float)), "'Thermostat' device missing numeric 'temperature'"
        elif dtype == "Lock":
            assert "locked" in device and isinstance(device["locked"], bool), "'Lock' device missing boolean 'locked' state"

    # Ensure all three device types are present
    for dtype, found in device_types.items():
        assert found, f"Device type '{dtype}' not found in response"

test_list_all_smart_home_devices()