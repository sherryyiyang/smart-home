import requests

BASE_URL = "http://localhost:3000"

def test_get_health_check_status_and_uptime():
    url = f"{BASE_URL}/health"
    headers = {
        "Accept": "application/json"
    }
    try:
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
    except requests.RequestException as e:
        assert False, f"Request to /health endpoint failed: {e}"

    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"
    try:
        data = response.json()
    except ValueError:
        assert False, "Response is not valid JSON"

    assert "status" in data, "Response JSON missing 'status' field"
    assert "uptime" in data, "Response JSON missing 'uptime' field"
    assert data["status"] == "ok", f"Expected status 'ok', got '{data['status']}'"
    assert isinstance(data["uptime"], (int, float)), f"Expected 'uptime' to be numeric, got {type(data['uptime'])}"
    assert data["uptime"] >= 0, f"Expected 'uptime' to be non-negative, got {data['uptime']}"

test_get_health_check_status_and_uptime()