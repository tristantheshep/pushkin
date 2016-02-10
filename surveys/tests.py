
from surveys.models import *

from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework.test import force_authenticate
from rest_framework import status

URLs = ['/surveys/','/surveys/1/','/surveys/1/questions/', '/surveys/1/questions/1', '/surveys/1/tags/', '/surveys/1/tags/1', '/surveys/1/responses/', '/surveys/1/responses/1', '/surveys/1/responses/1/answers/', '/surveys/1/responses/1/answers/1']


class TestBase(APITestCase):

    def setUp(self):
        User.objects.create(username='user1')
        User.objects.create(username='user2')
        User.objects.create(username='user3')

    def tearDown(self):
        self.users().delete()

    def users(self):
        return User.objects.all()


class AuthTests(TestBase):

    def test_unauthenticated_get(self):
        """
        HTTP requests are met with 403s if not authenticated on all URLs
        """
        requests = [self.client.get, self.client.post, self.client.put, self.client.patch, self.client.delete]
        for req in requests:
            for url in URLs:
                self.assertEqual(req(url).status_code, status.HTTP_403_FORBIDDEN,
                                 "Unauthenticated request %s/%s did not receive 403" % (req , url))

    def test_auth_token(self):
        """
        Users are automatically provided with auth tokens
        """
        [self.assertNotEqual(u.auth_token.key, "") for u in self.users()]

