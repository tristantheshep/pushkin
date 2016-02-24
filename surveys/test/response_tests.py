
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
        questions = ['question1', 'question2', 'question3']
        for question in questions:
            survey.questions.create(question_text=question)
        survey.publish()

        # Create the POST request on the submittal URL
        answers = ['answer1', 'answer2', 'answer3']
        response_data = {q:a for q, a in zip(questions, answers)}

        # Submit a few responses
        uri = '/submit/%s/' % survey.id
        self.client.post(uri, response_data)
        self.client.post(uri, response_data)
        self.client.post(uri, response_data)

        # Check the database now matches the request
        survey.refresh_from_db()
        self.assertEqual(survey.responses.count(), 3)
        self.assertEqual(response_data,
                         {q.question_text:a.answer_text
                          for q, a in zip(survey.questions.all(),
                                          survey.responses.first().answers.all())})
