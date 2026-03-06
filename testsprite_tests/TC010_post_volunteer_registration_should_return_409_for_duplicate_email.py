import requests
import uuid

BASE_URL = "http://localhost:8000"
VOLUNTEER_ENDPOINT = f"{BASE_URL}/volunteer/"
HEADERS = {"Content-Type": "application/json"}
TIMEOUT = 30

def test_post_volunteer_registration_should_return_409_for_duplicate_email():
    email = f"testuser-{uuid.uuid4()}@example.com"
    volunteer_data = {
        "name": "Test User",
        "email": email,
        "phone": "1234567890",
        "skills": "Testing",
        "preferred_area": "Area 1",
        "terms_accepted": True
    }

    try:
        # First registration: should succeed with 201 Created
        response1 = requests.post(VOLUNTEER_ENDPOINT, json=volunteer_data, headers=HEADERS, timeout=TIMEOUT)
        assert response1.status_code == 201, f"Expected 201 on first volunteer registration, got {response1.status_code}"
        response_json1 = response1.json()
        assert "id" in response_json1, "Response JSON missing 'id' on first registration"
        assert response_json1.get("status") == "pending", "Expected status 'pending' on first registration"

        # Second registration with same email: should fail with 409 Conflict
        response2 = requests.post(VOLUNTEER_ENDPOINT, json=volunteer_data, headers=HEADERS, timeout=TIMEOUT)
        assert response2.status_code == 409, f"Expected 409 on duplicate volunteer registration, got {response2.status_code}"
        response_json2 = response2.json()
        message = response_json2.get("message", "") or response_json2.get("detail", "")
        assert "email already registered" in message.lower(), "Expected error message to mention 'email already registered'"

    finally:
        # Cleanup: if first registration succeeded, delete volunteer record to keep test idempotent
        if 'response_json1' in locals() and "id" in response_json1:
            volunteer_id = response_json1["id"]
            try:
                delete_url = f"{VOLUNTEER_ENDPOINT}{volunteer_id}/"
                requests.delete(delete_url, timeout=TIMEOUT)
            except Exception:
                pass


test_post_volunteer_registration_should_return_409_for_duplicate_email()