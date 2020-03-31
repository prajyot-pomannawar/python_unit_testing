from django.test import TestCase, Client
from django.urls import resolve, reverse


class URLTestCase(TestCase):

    def test_view_all_user_url(self):
        path = reverse('view_all_users')
        self.assertEqual(resolve(path).view_name, 'view_all_users')