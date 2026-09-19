from pathlib import Path

from django.test import TestCase


class SiteSmokeTests(TestCase):
    def test_homepage_route_is_available(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_about_route_is_available(self):
        response = self.client.get('/about/overview/')
        self.assertEqual(response.status_code, 200)

    def test_main_js_avoids_invalid_hash_selector(self):
        js_path = Path(__file__).resolve().parent.parent / 'static' / 'js' / 'main.js'
        content = js_path.read_text(encoding='utf-8')
        self.assertNotIn('a[href^="#"]', content)
