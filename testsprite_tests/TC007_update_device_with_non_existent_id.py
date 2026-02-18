import requests

BASE_URL = "http://localhost:3000"

def test_update_device_with_non_existent_id():
    non_existent_id = "nonexistent123456"
    url = f"{BASE_URL}/devices/{non_existent_id}"
    payload = {"on": True}
    headers = {"Content-Type": "application/json"}

    try:
        response = requests.patch(url, json=payload, headers=headers, timeout=30)
    except requests.RequestException as e:
        assert False, f"Request failed: {e}"

    assert response.status_code == 404, f"Expected status code 404 but got {response.status_code}"
    try:
        json_response = response.json()
    except ValueError:
        assert False, "Response is not valid JSON"

    assert "error" in json_response or "message" in json_response, "Response JSON does not contain error or message key"

    error_message = json_response.get("error") or json_response.get("message")
    assert isinstance(error_message, str), "Error message is not a string"
    assert "Device" in error_message and "not found" in error_message, f"Expected error message to contain 'Device' and 'not found' but got '{error_message}'"

test_update_device_with_non_existent_id()