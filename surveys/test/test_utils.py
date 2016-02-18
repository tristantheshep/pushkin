
""" Utilities to help with testing this app """

from django.contrib.auth.models import User

from rest_framework.test import APITestCase

class TestBase(APITestCase):
    """ A base class that provides functionality of the `APITestCase` class
    as well as a few other utils specific to Pushkin
    """

    def setUp(self):
        """
        Performs a basic multi-user database setup with which to test and
        authenticates one of the users.

        The resulting database is composed of two users, each with two surveys,
        each with two tag options, questions, and responses.

        The users are contained in self.users[]. The first user is
        authenticated.
        """
        # Create a couple of users
        for i in range(2):
            # pylint: disable=no-member
            user = User.objects.create(username='user_' + str(i))
            # Add a couple of surveys for each user
            for j in range(2):
                survey = user.surveys.create(name=user.username + '_survey_' + \
                                             str(j))
                survey.publish()
                # Add a couple of tags, questions, responses to each survey
                for k in range(2):
                    survey.tag_options.create(tag_text=survey.name +           \
                                              '_tag_opt_' + str(k))
                    survey.questions.create(question_text=survey.name +        \
                                            '_question_' + str(k))
                    survey.responses.create()


        # Authenticate requests from the first user by default
        # pylint: disable=no-member
        self.client.force_authenticate(user=self.users[0])

        # Generate a list of all URIs for two of the users
        user1, user2, *_ = self.users
        self.user1_uris = _all_user_uris(user1)
        self.user2_uris = _all_user_uris(user2)

        # Keep a list of requests handy
        self.requests = [self.client.get, self.client.post, self.client.put,
                         self.client.patch, self.client.delete]

        from surveys.models import Survey

    def tearDown(self):
        """ Delete the database created for these tests """
        self.users.delete()

    @property
    def users(self):
        """ A property to return all Users in the test database """
        return User.objects.all() # pylint: disable=no-member

    def check_response_code(self, uri, method, exp_response_codes):
        """
        Assert we get a certain response code given a URI and http method
        """
        response_code = method(uri).status_code
        self.assertIn(response_code, exp_response_codes,
                      "Expected one of %s for request '%s %s', got %s"
                      % (exp_response_codes, method.__name__,
                         uri, response_code))

    def check_response_code_not(self, uri, method, not_exp_response_codes):
        """
        Assert we do NOT get a given response for a uri/method
        """

        response_code = method(uri).status_code
        self.assertNotIn(response_code, not_exp_response_codes,
                         "Did not expect %s for request '%s %s'"
                         % (response_code, method.__name__, uri))


def _all_user_uris(user):
    """
    Generate a list of all URIs for a given user, e.g. all surveys,
    all questions for each survey, etc.
    """
    uris = []
    for survey in user.surveys.all():
        survey_uri = '/surveys/%s/' % survey.id
        questions_uri = survey_uri + 'questions/'
        tags_uri = survey_uri + 'tags/'
        responses_uri = survey_uri + 'responses/'

        uris.append(survey_uri)
        uris.append(questions_uri)
        uris.append(tags_uri)
        uris.append(responses_uri)

        for i in range(1, survey.questions.count() + 1):
            uris.append(questions_uri + '%s/' % i)

        for i in range(1, survey.tag_options.count() + 1):
            uris.append(tags_uri + '%s/' % i)

        for i, response in enumerate(survey.responses.all()):
            response_uri = responses_uri + '%s/' % (i+1)
            answers_uri = response_uri + 'answers/'
            uris.append(response_uri)
            uris.append(answers_uri)

            for j in range(1, response.answers.count() + 1):
                uris.append(answers_uri + '%s/' % j)

    return uris

