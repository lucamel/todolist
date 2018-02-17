from django.http import HttpRequest
from django.test import TestCase
from django.urls import resolve

from lists.views import home_page

class HomePageTest(TestCase):

    def test_root_url_resolves_to_home_page_view(self):
        found = resolve('/')
        self.assertEqual(found.func, home_page)

    def test_home_page_is_about_todo_lists(self):
        request = HttpRequest()

        response = home_page(request)

        with open('lists/templates/home.html') as f:
            expected_content = f.read()

        self.assertEqual(response.content.decode(), expected_content)