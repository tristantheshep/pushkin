
""" Tests for the respondent UI """

import requests

from django.contrib.auth.models import User
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.firefox.webdriver import WebDriver

class UIRespondentTests(StaticLiveServerTestCase):
    """ Tests for the UI presented to the survey respondents. These include
    page rendering, response submission, and the CSRF protection of the page"""

    def setUp(self):
        """ Set up for the UI/respondent test case """
        super(UIRespondentTests, self).setUp()
        self.web_driver = WebDriver()

        # Create a new survey, add some questions, and publish
        user = User.objects.create(username='humphrey')
        survey = user.surveys.create(name='foobar')
        questions = ['what?', 'where?', 'why?', 'when?', 'anything else?']
        for question in questions:
            survey.questions.create(question_text=question)
        survey.publish()
        self.survey = survey

        # Load up the response page
        url = '%s%s%s/' % (self.live_server_url, '/respond/', survey.id)
        self.web_driver.get(url)

        # No way of checking directly for 404 in selenium; just make sure the
        # survey name is in the source
        self.assertIn('foobar', self.web_driver.page_source)

    def tearDown(self):
        """ Clean up for the UI/respondent test case """
        self.web_driver.quit()
        super(UIRespondentTests, self).tearDown()

        User.objects.all().delete()

    def test_response_page_rendering(self):
        """ The response page for a a survey contains the correct questions,
        in order
        """
        try:
            form = self.web_driver.find_element_by_name('survey-respond-%s' %
                                                        self.survey.id)
        except NoSuchElementException:
            self.fail('The form did not render with the expected element name')

        # For every question in the DB, make sure the page contains an element
        # for each, with the name as the question's ordinance and the id as
        # the question's pk.
        for question_ix, question in enumerate(self.survey.questions.all()):
            try:
                e1 = self.web_driver.find_element_by_name(str(question_ix))
            except NoSuchElementException:
                self.fail('Question index %s was not rendered in response page'
                            % question_ix)
            try:
                e2 = self.web_driver.find_element_by_id(str(question.pk))
            except NoSuchElementException:
                self.fail('Question pk %s was not rendered in response page'
                             % question.pk)

            if e1 != e2:
                self.fail('Expected HTML element for question pk %s and id %s '
                          'to match' % (question.pk, question_ix))

    def test_response_submission(self):
        """ A submission of a valid form creates the expected `Response` and
        `Answer` entries in the database
        """
        questions = self.survey.questions.all()
        for question_ix, question in enumerate(questions):
            ans_input = self.web_driver.find_element_by_name(str(question_ix))
            ans_input.send_keys('Answer to "%s"' % question.question_text)

        submit_button = self.web_driver.find_element_by_name('submit-response')
        submit_button.click()

        answers = self.survey.responses.get().answers.all()
        self.assertEqual(len(answers), len(questions))
        for question, answer in zip(questions, answers):
           self.assertEqual(answer.answer_text,
                            'Answer to "%s"' % question.question_text)

    def test_csrf_protection(self):
        """ POST requests made outside of the form are rejected """
        response = requests.post('%s%s%s/' % (self.live_server_url,
                                              '/respond/',
                                              self.survey.id))
        self.assertEqual(response.status_code, 403)
        self.assertIn("this site requires a CSRF cookie when submitting forms",
                      response.text)
