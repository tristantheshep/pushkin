
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

    def test_publication_by_api(self):
        """ A survey is published by the appropriate data message, and
        requests to unpublish are ignored.
         """
        survey = self.users[0].surveys.create()
        self.assertEqual(survey.published, False)
        self.check_response_code('/surveys/%s/' % survey.id,
                                 self.client.patch, [status.HTTP_200_OK],
                                 {"published":True})
        survey.refresh_from_db()
        self.assertEqual(survey.published, True)

