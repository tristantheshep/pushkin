
""" The top-level test runner for this app """

# Import any test suites to run here
# pylint: disable=unused-import
from .test.response_tests import ResponseTests
from .test.auth_tests import AuthTests, RegistrationTests
from .test.api_tests import APITests
from .test.db_tests import DBLogicTests
from .test.ui_respondent import UIRespondentTests

