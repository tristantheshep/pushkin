
""" Tests the API itself; http codes and response bodies """

from rest_framework import status

from .test_utils import TestBase


class APITests(TestBase):
    """ Tests concerning serialized responses and HTTP codes """

    def test_unpublished_response(self):
        """ A 403 is returned when responding to an unpublished survey """
        survey = self.users[0].surveys.create()
        self.check_response_code('/surveys/%s/responses/' % survey.id,
                                 self.client.post, [status.HTTP_403_FORBIDDEN])

        # Publish the survey and check that we now get a 201
        survey.publish()
        self.check_response_code('/surveys/%s/responses/' % survey.id,
                                 self.client.post, [status.HTTP_201_CREATED])
