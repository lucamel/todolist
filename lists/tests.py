from django.http import HttpRequest
from django.template.loader import render_to_string
from django.urls import resolve
from django.test import TestCase

from lists.views import home_page

class HomePageTest(TestCase):

    def test_home_page_is_about_todo_lists(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')