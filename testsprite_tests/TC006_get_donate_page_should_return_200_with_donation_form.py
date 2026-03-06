import requests

def test_get_donate_page_should_return_200_with_donation_form():
    base_url = "http://localhost:8000"
    url = f"{base_url}/donate/"
    headers = {
        "Accept": "text/html",
    }
    try:
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
    except requests.RequestException as e:
        assert False, f"Request failed: {e}"

    assert response.status_code == 200, f"Expected status code 200 but got {response.status_code}"

    content = response.text.lower()

    assert 'minimum donation' in content or 'minimum' in content, "Minimum donation info not found in response HTML"
    assert 'suggested amounts' in content or 'suggested' in content, "Suggested amounts info not found in response HTML"
    assert 'upi' in content, "UPI apps info not found in response HTML"


test_get_donate_page_should_return_200_with_donation_form()