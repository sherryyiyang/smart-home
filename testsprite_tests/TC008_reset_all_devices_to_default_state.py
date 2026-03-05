import requests

BASE_URL = "http://localhost:3000"
TIMEOUT = 30

def test_reset_all_devices_to_default_state():
    url = f"{BASE_URL}/reset"
    headers = {"Content-Type": "application/json"}

    try:
        response = requests.post(url, headers=headers, timeout=TIMEOUT)
        assert response.status_code == 200, f"Expected status 200, got {response.status_code}"
        json_resp = response.json()
        assert "message" in json_resp, "Response JSON does not contain 'message'"
        assert isinstance(json_resp["message"], str), "'message' is not a string"
        assert "reset" in json_resp["message"].lower(), "Confirmation message does not indicate reset"
    except requests.RequestException as e:
        assert False, f"Request failed: {e}"

test_reset_all_devices_to_default_state()