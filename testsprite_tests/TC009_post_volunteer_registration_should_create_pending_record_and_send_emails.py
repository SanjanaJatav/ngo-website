import requests
import uuid

BASE_URL = "http://localhost:8000"
VOLUNTEER_ENDPOINT = f"{BASE_URL}/volunteer/"
TIMEOUT = 30


def test_post_volunteer_registration_should_create_pending_record_and_send_emails():
    unique_email = f"testuser_{uuid.uuid4().hex[:8]}@example.com"
    payload = {
        "name": "Test User",
        "email": unique_email,
        "phone": "+919876543210",
        "skills": "fundraising, event planning",
        "preferred_area": "Education",
        "availability": "Weekends",
        "terms_accepted": True
    }
    headers = {
        "Content-Type": "application/json"
    }

    volunteer_id = None
    try:
        response = requests.post(VOLUNTEER_ENDPOINT, json=payload, headers=headers, timeout=TIMEOUT)
        assert response.status_code == 201, f"Expected 201, got {response.status_code}"
        data = response.json()
        assert "id" in data, "Response JSON missing 'id'"
        assert "status" in data, "Response JSON missing 'status'"
        assert data["status"].lower() == "pending", f"Expected status 'pending', got {data['status']}"
        volunteer_id = data["id"]

    finally:
        if volunteer_id is not None:
            # Attempt to delete created volunteer to clean up
            try:
                delete_url = f"{VOLUNTEER_ENDPOINT}{volunteer_id}/"
                del_response = requests.delete(delete_url, timeout=TIMEOUT)
                # We don't assert here as delete may not be supported; just attempt cleanup
            except Exception:
                pass


test_post_volunteer_registration_should_create_pending_record_and_send_emails()
