import requests

BASE_URL = "http://localhost:8000"
TIMEOUT = 30

# Using hardcoded minimum donation value and payment_app string as per PRD, because GET /donate/ returns HTML, not JSON

def test_post_donate_should_create_pending_donation_and_return_201():
    minimum_donation = 10  # Assuming minimum donation is 10 as per PRD example
    payment_app = "googlepay"  # Using a valid payment_app string from the PRD example

    payload = {
        "donor_name": "Test Donor",
        "donor_email": "testdonor@example.com",
        "amount": minimum_donation,
        "payment_app": payment_app
    }
    headers = {"Content-Type": "application/json"}

    try:
        post_response = requests.post(f"{BASE_URL}/donate/", json=payload, headers=headers, timeout=TIMEOUT)
    except requests.RequestException as e:
        assert False, f"POST /donate/ failed: {e}"

    assert post_response.status_code == 201, f"Expected status code 201 but got {post_response.status_code}"

    try:
        resp_json = post_response.json()
    except Exception as e:
        assert False, f"Response is not valid JSON: {e}"

    assert "transaction_reference" in resp_json and isinstance(resp_json["transaction_reference"], str) and resp_json["transaction_reference"].strip() != "", \
        "transaction_reference missing or invalid in response"
    assert "upi_deep_link" in resp_json and isinstance(resp_json["upi_deep_link"], str) and resp_json["upi_deep_link"].startswith("upi://pay"), \
        "upi_deep_link missing or invalid in response"


test_post_donate_should_create_pending_donation_and_return_201()
