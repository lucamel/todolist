from django.http import HttpRequest
from django.template.loader import render_to_string
from django.urls import resolve
from django.test import TestCase

from lists.models import Item
from lists.views import home_page


class HomePageTest(TestCase):

    def test_home_page_is_about_todo_lists(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')

    def test_can_save_a_POST_request(self):
        self.client.post('/', {'item_text': 'A new item'})
        self.assertEqual(Item.objects.count(), 1)      
        new_item = Item.objects.first()      
        self.assertEqual(new_item.text, 'A new item')
        
    def test_redirects_after_POST(self):
        response = self.client.post('/', {'item_text': 'A new item'})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['location'], '/lists/the-only-list-in-the-world/')


class ListViewTest(TestCase):

    def test_uses_list_template(self):
        response = self.client.get('/lists/the-only-list-in-the-world/')
        self.assertTemplateUsed(response, 'list.html')

    def test_displays_all_items(self):
        Item.objects.create(text='Item 1')
        Item.objects.create(text='Item 2')

        response = self.client.get('/lists/the-only-list-in-the-world/')

        self.assertContains(response, 'Item 1')
        self.assertContains(response, 'Item 2')


class ItemModelTest(TestCase):

    def test_saving_and_retrieving_items(self):
        first_item = Item()
        first_item.text = 'Item the first'
        first_item.save()

        second_item = Item()
        second_item.text = 'Item the second'
        second_item.save()

        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)

        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]
        self.assertEqual(first_saved_item.text, 'Item the first')
        self.assertEqual(second_saved_item.text, 'Item the second')

    def test_only_saves_items_when_necessary(self):
        self.client.get('/')
        self.assertEqual(Item.objects.count(), 0)