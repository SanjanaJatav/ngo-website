import requests

BASE_URL = "http://localhost:8000"
TIMEOUT = 30

def test_get_our_work_listing_should_return_200_with_pagination_and_filters():
    url = f"{BASE_URL}/our-work/"
    params = {
        "category": "education",
        "status": "completed",
        "page": 1
    }
    headers = {
        "Accept": "application/json"
    }

    try:
        response = requests.get(url, params=params, headers=headers, timeout=TIMEOUT)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        assert False, f"Request failed: {e}"

    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"

    try:
        data = response.json()
    except ValueError:
        assert False, "Response is not valid JSON"

    # Validate presence of expected keys
    assert "projects" in data, "'projects' key not found in response"
    assert "categories" in data, "'categories' key not found in response"
    assert "statistics" in data, "'statistics' key not found in response"

    # Validate 'projects' is a dict containing pagination info and results
    projects = data["projects"]
    assert isinstance(projects, dict), "'projects' should be a dictionary"
    assert "count" in projects, "'count' key missing in projects"
    assert "next" in projects, "'next' key missing in projects"
    assert "previous" in projects, "'previous' key missing in projects"
    assert "results" in projects, "'results' key missing in projects"
    assert isinstance(projects["results"], list), "'results' should be a list"

    # Validate 'categories' is a list
    categories = data["categories"]
    assert isinstance(categories, list), "'categories' should be a list"

    # Validate 'statistics' is a dict with numeric values
    statistics = data["statistics"]
    assert isinstance(statistics, dict), "'statistics' should be a dictionary"
    for key, value in statistics.items():
        assert isinstance(value, (int, float)), f"Statistic '{key}' should be numeric"

test_get_our_work_listing_should_return_200_with_pagination_and_filters()
