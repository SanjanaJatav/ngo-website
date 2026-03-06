import requests

BASE_URL = "http://localhost:8000"
TIMEOUT = 30

def test_get_about_team_should_return_200_with_active_team_members():
    url = f"{BASE_URL}/about/team/"
    try:
        response = requests.get(url, timeout=TIMEOUT)
        response.raise_for_status()
    except requests.RequestException as e:
        assert False, f"Request failed: {e}"

    assert response.status_code == 200, f"Expected status code 200 but got {response.status_code}"

    content = response.text

    # Check that key expected strings exist in HTML content indicating leadership and team members sections
    assert "leadership" in content.lower(), "Response content missing 'leadership' section"
    assert "team" in content.lower(), "Response content missing 'team' section"


test_get_about_team_should_return_200_with_active_team_members()