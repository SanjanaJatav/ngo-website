import requests

def test_get_about_overview_should_return_200_with_mission_and_vision():
    base_url = "http://localhost:8000"
    url = f"{base_url}/about/overview/"
    headers = {
        "Accept": "application/json"
    }
    try:
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        data = response.json()
    except requests.exceptions.RequestException as e:
        assert False, f"Request to {url} failed: {e}"
    except ValueError:
        assert False, f"Response from {url} is not valid JSON"
    # Validate HTTP 200 status
    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"
    # Validate required keys in JSON response
    required_keys = ["about_overview", "mission_statement", "vision_statement", "years_of_operation"]
    missing_keys = [key for key in required_keys if key not in data]
    assert not missing_keys, f"Missing keys in response JSON: {missing_keys}"
    # Validate non-empty values for these keys
    for key in required_keys:
        assert data[key] is not None and data[key] != "", f"Value for '{key}' is empty or None"

test_get_about_overview_should_return_200_with_mission_and_vision()