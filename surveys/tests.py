
from surveys.models import *

from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework.test import force_authenticate
from rest_framework import status

URLs = ['/surveys/','/surveys/1/','/surveys/1/questions/', '/surveys/1/questions/1', '/surveys/1/tags/', '/surveys/1/tags/1', '/surveys/1/responses/', '/surveys/1/responses/1', '/surveys/1/responses/1/answers/', '/surveys/1/responses/1/answers/1']


class TestBase(APITestCase):

    def setUp(self):
        user0 = User.objects.create(username='user0')
        user1 = User.objects.create(username='user1')
        user2 = User.objects.create(username='user2')

        # Add some surveys to user1
        user1.surveys.create(name='survey1_1')
        user1.surveys.create(name='survey1_2')
        user1.surveys.create(name='survey1_3')

        # Authenticate requests from user0
        self.client.force_authenticate(user=user0)

    def tearDown(self):
        self.users.delete()

    @property
    def users(self):
        return User.objects.all()


class AuthTests(TestBase):

    def test_unauthenticated_requests(self):
        """
        HTTP requests are met with 403s if not authenticated on all URLs
        """
        # Remove authentication from client
        self.client.force_authenticate()

        requests = [self.client.get, self.client.post, self.client.put, self.client.patch, self.client.delete]
        for req in requests:
            for url in URLs:
                self.assertEqual(req(url).status_code, status.HTTP_403_FORBIDDEN,
                                 "Unauthenticated request %s/%s did not receive 403" % (req , url))

    def test_auth_token(self):
        """
        Users are automatically provided with auth tokens
        """
        [self.assertNotEqual(u.auth_token.key, "") for u in self.users]

    def test_get_unowned_survey(self):
        """
        User is met with 403 when trying to access another user's survey
        """
        # Get a survey from user1 (we are authenticated as user0)
        survey_id = self.users[1].surveys.all()[0].id
        uri = '/surveys/%s/' % survey_id
        response = self.client.get(uri).status_code
        self.assertEqual(response, status.HTTP_403_FORBIDDEN,
                         "Expected 403 for GET request on %s, got %s" % 
                                                                (uri, response))        



