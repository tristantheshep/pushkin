
""" Tests for the database layer """

from django.contrib.auth.models import User

from .test_utils import TestBase

class DBLogicTests(TestBase):
    """
    Concernins pure database logic. These tests are performed directly at the
    DB layer and do not involve HTTP requests.
    """

    def test_automatic_answer_creation(self):
        """
        When a response is created, answers objects are automatically create
        beneath. A response should contain as many answers as there are
        questions in the survey.
        """
        survey = self.users[0].surveys.create(name='My Survey')
        questions = ['who', 'what', 'where', 'why', 'when']
        for question in questions:
            survey.questions.create(question_text=question)

        resp = survey.responses.create()
        self.assertEqual(len(questions), resp.answers.count())
        self.assertTrue(all(a.answer_text == '' for a in resp.answers.all()))

    def test_survey_creation(self):
        """
        Test general survey creation
        """
        user = User.objects.first() # pylint: disable=no-member
        survey = user.surveys.create()
        self.assertEqual(survey.name, 'My Survey')
        self.assertEqual(survey.owner, user)
        self.assertEqual(survey.questions.count(), 0)
        self.assertEqual(survey.responses.count(), 0)
        self.assertEqual(survey.tag_options.count(), 0)
        self.assertEqual(survey.published, False)
