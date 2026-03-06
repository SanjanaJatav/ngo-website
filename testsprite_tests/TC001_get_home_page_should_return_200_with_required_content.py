import requests

def test_get_home_page_should_return_200_with_required_content():
    base_url = "http://localhost:8000"
    url = f"{base_url}/"
    headers = {
        "Accept": "text/html",
    }
    try:
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
    except requests.RequestException as e:
        assert False, f"GET / request failed: {e}"

    # Assert HTTP 200 status
    assert response.status_code == 200, f"Expected status code 200 but got {response.status_code}"

    content = response.text
    # Check presence of indicative content related to required elements in the HTML
    assert "slider" in content.lower(), "Slider section not found in response content"
    assert "site settings" in content.lower() or "site-setting" in content.lower() or "site_settings" in content.lower(), "Site settings section not found in response content"
    assert "featured" in content.lower(), "Featured projects section not found in response content"
    assert "statistic" in content.lower() or "impact" in content.lower(), "Statistics section not found in response content"

test_get_home_page_should_return_200_with_required_content()