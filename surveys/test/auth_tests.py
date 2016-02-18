
""" Tests for authentication, permissions, and security """

from rest_framework import status

from .test_utils import TestBase


class AuthTests(TestBase):
    """ Tests concerning authentication and HTTP codes """

    def test_unauthenticated_requests(self):
        """ All HTTP requests on all URIs are met with 403s if not authenticated
        """
        # Remove authentication from client
        self.client.force_authenticate() # pylint: disable=no-member

        for uri in self.user1_uris + self.user2_uris + ['/surveys/']:
            for req in self.requests:
                self.check_response_code(uri, req, [status.HTTP_403_FORBIDDEN])

    def test_auth_token(self):
        """ Users are automatically provided with auth tokens """
        users = self.users
        keys = set(u.auth_token.key for u in users)
        self.assertEqual(len(keys), len(users), "Some users have the same key")

    def test_own_survey_access(self):
        """ User is not 403'd when accessing their own URIs """
        for uri in self.user1_uris:
            # Check for explicit 200s when getting
            self.check_response_code(uri, self.client.get, [status.HTTP_200_OK])

            # Just check that the other requests aren't 403d - we don't care
            # about anything other than permissions for these auth tests
            for req in self.requests:
                if req != self.client.delete:
                    self.check_response_code_not(uri, req,
                                                 [status.HTTP_403_FORBIDDEN])

    def test_others_survey_access(self):
        """ User is met with 403 when trying to access another user's URIs """
        for uri in self.user2_uris:
            for req in [self.client.get]:
                self.check_response_code(uri, req,
                                         [status.HTTP_403_FORBIDDEN,
                                          status.HTTP_405_METHOD_NOT_ALLOWED])

