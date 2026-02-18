import requests

BASE_URL = "http://localhost:3000"

def test_handle_internal_error_on_reset_endpoint():
    url = f"{BASE_URL}/reset"
    try:
        response = requests.post(url, timeout=30)
        # We expect a 500 status code in case of internal server error
        assert response.status_code == 500, f"Expected status code 500 but got {response.status_code}"
        json_resp = response.json()
        # The server error message should be present in the response
        assert isinstance(json_resp, dict), "Response is not a JSON object"
        error_message = json_resp.get("message", "").lower()
        assert "error" in error_message or "server" in error_message, \
            f"Expected error message containing 'error' or 'server', got: {json_resp.get('message')}"
    except requests.RequestException as e:
        assert False, f"Request failed with exception: {e}"

test_handle_internal_error_on_reset_endpoint()