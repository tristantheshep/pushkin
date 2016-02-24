
""" Tests the UI/submitting of survey responses """

from .test_utils import TestBase

class ResponseTests(TestBase):
    """ Tests for the respondents' endpoint """

    def test_response(self):
        """ A response can be submitted by an unauthorized user """
        # Remove existing authorization
        self.client.force_authenticate() # pylint: disable=no-member

        # Create a survey with questions
        survey = self.users[0].surveys.create()
        questions = ['question 1', 'question 2', 'question 3']
        for question in questions:
            survey.questions.create(question_text=question)
        survey.publish()

        # Create the POST request on the submittal URL
        answers = ['answer 1', 'answer 2', 'answer 3']
        response_data = {i : a for i, a in enumerate(answers)}

        # Submit a few responses
        uri = '/submit/%s/' % survey.id
        self.client.post(uri, response_data)
        self.client.post(uri, response_data)
        self.client.post(uri, response_data)

        # Check the database now matches the request
        survey.refresh_from_db()
        self.assertEqual(survey.responses.count(), 3)
        self.assertEqual(response_data,
                         {i : a.answer_text
                          for i, a in
                             enumerate(survey.responses.first().answers.all())})
