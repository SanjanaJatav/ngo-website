import requests

BASE_URL = "http://localhost:8000"
TIMEOUT = 30
DONATE_ENDPOINT = f"{BASE_URL}/donate/"


def test_post_donate_should_return_400_for_invalid_amount_or_missing_fields():
    session = requests.Session()
    # First GET to obtain CSRF cookie
    try:
        get_resp = session.get(DONATE_ENDPOINT, timeout=TIMEOUT)
        get_resp.raise_for_status()
    except Exception as e:
        assert False, f"Initial GET request failed with exception: {e}"

    # Extract CSRF token from cookies
    csrf_token = session.cookies.get('csrftoken')
    assert csrf_token is not None, "CSRF token cookie not found in initial GET response"

    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "X-CSRFToken": csrf_token
    }

    test_payloads = [
        # amount less than minimum_donation (MINIMUM_DONATION=100 per PRD)
        {"donor_name": "Test Donor", "donor_email": "test@example.com", "amount": "0", "payment_app": "other"},
        {"donor_name": "Test Donor", "donor_email": "test@example.com", "amount": "1", "payment_app": "googlepay"},
        # missing donor_name
        {"donor_email": "test@example.com", "amount": "150", "payment_app": "phonepe"},
        # missing donor_email
        {"donor_name": "Test Donor", "amount": "150", "payment_app": "bhim"},
        # missing amount
        {"donor_name": "Test Donor", "donor_email": "test@example.com", "payment_app": "paytm"},
        # missing payment_app
        {"donor_name": "Test Donor", "donor_email": "test@example.com", "amount": "150"},
        # all missing
        {}
    ]

    for payload in test_payloads:
        try:
            response = session.post(DONATE_ENDPOINT, data=payload, headers=headers, timeout=TIMEOUT)
        except Exception as e:
            assert False, f"Request failed with exception: {e}"
        else:
            assert response.status_code == 400, (
                f"Expected HTTP 400 for payload {payload}, got {response.status_code} with body {response.text}"
            )
            # Validate that response contains validation error messages
            try:
                json_resp = response.json()
            except Exception:
                assert False, "Response is not valid JSON"
            else:
                assert isinstance(json_resp, dict), "Response JSON should be an object/dictionary"
                # At least one validation error key should be present
                assert any(k in json_resp for k in ("donor_name", "donor_email", "amount", "payment_app", "detail", "error")), (
                    f"Validation errors not found in response JSON: {json_resp}"
                )


test_post_donate_should_return_400_for_invalid_amount_or_missing_fields()
