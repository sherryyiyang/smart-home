import requests

BASE_URL = "http://localhost:3000"
TIMEOUT = 30

def test_get_single_device_by_invalid_id():
    invalid_id = "nonexistent-device-id-12345"
    url = f"{BASE_URL}/devices/{invalid_id}"
    try:
        response = requests.get(url, timeout=TIMEOUT)
    except requests.RequestException as e:
        assert False, f"Request failed: {e}"

    assert response.status_code == 404, f"Expected status code 404, got {response.status_code}"
    try:
        json_resp = response.json()
    except ValueError:
        assert False, "Response is not valid JSON"

    assert "error" in json_resp or "message" in json_resp, "Response JSON should contain error or message field"
    error_message = json_resp.get("error") or json_resp.get("message")
    assert "Device" in error_message and "not found" in error_message, f"Expected error message to contain 'Device' and 'not found', got '{error_message}'"

test_get_single_device_by_invalid_id()
