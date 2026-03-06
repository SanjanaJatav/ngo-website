import requests
import time

BASE_URL = "http://localhost:8000"
TIMEOUT = 30


def test_get_our_work_detail_should_return_200_and_increment_views():
    # First, get a list of projects to find a valid slug to test with
    try:
        response_list = requests.get(f"{BASE_URL}/our-work/", timeout=TIMEOUT)
        response_list.raise_for_status()
        projects_data = response_list.json()
        projects = projects_data.get("results") or projects_data.get("projects") or []
        if not projects:
            raise AssertionError("No projects available to test with.")
        slug = projects[0].get("slug")
        assert slug, "Project slug is missing"
    except Exception as e:
        raise AssertionError(f"Failed to get project slug for test: {e}")

    # Get detail first time to check views_count initial value
    url = f"{BASE_URL}/our-work/{slug}/"
    try:
        response1 = requests.get(url, timeout=TIMEOUT)
        response1.raise_for_status()
        data1 = response1.json()
        assert "project" in data1 or "id" in data1 or "slug" in data1, "Project detail missing"
        assert isinstance(data1.get("gallery_images"), list), "gallery_images is missing or not a list"
        assert isinstance(data1.get("related_projects"), list), "related_projects is missing or not a list"
        views_count_1 = data1.get("views_count")
        assert isinstance(views_count_1, int), "views_count is missing or not an integer"
    except Exception as e:
        raise AssertionError(f"Failed at first GET /our-work/<slug>/: {e}")

    # Wait briefly to allow view count to increment if async (depending on implementation)
    time.sleep(1)

    # Get detail second time to verify views_count incremented
    try:
        response2 = requests.get(url, timeout=TIMEOUT)
        response2.raise_for_status()
        data2 = response2.json()
        views_count_2 = data2.get("views_count")
        assert isinstance(views_count_2, int), "views_count is missing or not an integer on second call"
        assert views_count_2 == views_count_1 + 1, f"views_count did not increment as expected: first={views_count_1}, second={views_count_2}"
    except Exception as e:
        raise AssertionError(f"Failed at second GET /our-work/<slug>/: {e}")


test_get_our_work_detail_should_return_200_and_increment_views()