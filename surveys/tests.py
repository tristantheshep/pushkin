
from surveys.models import *
from surveys.views import *

from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework.test import force_authenticate
from rest_framework import status

URLs = ['/surveys/','/surveys/1/','/surveys/1/questions/', '/surveys/1/questions/1', '/surveys/1/tags/', '/surveys/1/tags/1', '/surveys/1/responses/', '/surveys/1/responses/1', '/surveys/1/responses/1/answers/', '/surveys/1/responses/1/answers/1']

class AuthTests(APITestCase):
    def test_unauthenticated_get(self):
        for url in URLs:
            self.assertEqual(self.client.get(url).status_code, status.HTTP_403_FORBIDDEN,
                             "Unauthenticated get request did not receive 403 for url %s" % url)

