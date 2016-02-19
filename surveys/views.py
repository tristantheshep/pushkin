
""" The various views for the survey URLs """

from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.core import exceptions
from django.http import Http404
from django.views.generic import FormView
from rest_framework import generics
from rest_framework import permissions

from .models import DBError, Survey, Tag
from .serializers import (SurveySerializer, ResponseSerializer,
                          QuestionSerializer, AnswerSerializer, TagSerializer)


def survey_context(func):
    """
    Decorator to provide a shortcut to retrieve the appropriate `Survey` object
    given the identifier in a URI.

    Example:- to have the ResponseList view provide a queryset of all responses
              for the survey specified in the URI and the current user:

              @survey_context
                  def get_queryset(self, survey):
                  return survey.responses.all()

              Results in /survey/<survey_id>/responses/ returning the
              equivalent of  Surveys.get(id=<survey_id>).responses.all().

    403 permission errors are thrown if a user tries to access any survey they
    do not own (whether it actually exists or not)

    404s are thrown if the survey exists but any object under that survey is
    not found

    Example:- if only 3 responses exist under a survey, then accessing
              /survey/<id>/responses/4 will result in an indexerror as
              ResponseDetail.get_object() will assume survey.responses.all()[3]
              to exist.
    """

    def query_wrapper(view):
        """ The wrapped query to return """
        try:
            survey = Survey.objects.get(id=view.kwargs['sid'], owner=view.request.user)
            return func(view, survey)
        except Survey.DoesNotExist:
            raise exceptions.PermissionDenied
        except IndexError:
            raise Http404

    return query_wrapper


def uri2ix(view, key):
    """ Maps an ordinal number string from a URI to an actual index

    Example:- /surveys/<id>/responses/1 translates to 'get the first response
              for survey with ID <id>', which translates into Python as
              survey.responses.all()[0]
    """
    return int(view.kwargs[key]) - 1


class SurveyList(generics.ListCreateAPIView):
    """ A list of `Survey` objects. The queryset is limited to surveys of which
    the request maker is the owner

    Attributes:
        serializer_class      The serializer used for the objects in this view
        permission_classes    The required permissions to access this view
    """

    serializer_class = SurveySerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return Survey.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


# pylint: disable=too-many-ancestors
class SurveyDetail(generics.RetrieveUpdateDestroyAPIView):
    """ The view for an individual survey

    Attributes:
        serializer_class      The serializer used for the objects in this view
        permission_classes    The required permissions to access this view
    """

    serializer_class = SurveySerializer
    permission_classes = (permissions.IsAuthenticated,)

    @survey_context
    def get_object(self, survey): # pylint: disable=arguments-differ
        return survey


class ResponseList(generics.ListCreateAPIView):
    """ The view for survey's list of responses. The queryset is limited
    to a specific survey, as identified in the URI

    Attributes:
        serializer_class      The serializer used for the objects in this view
        permission_classes    The required permissions to access this view
    """

    serializer_class = ResponseSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def perform_create(self, serializer):
        """ Overrides Response creation from validated data. This allows for
        creations from data that will look like:

        { 'answer_strings' : [<answer_string>, <answer_string>, ...] }

        To automatically create a `Response` with the appropriate 'Answer'
        objects in the `Response.answers` field.
        """
        try:
            # Cut answer_strings from the validated data, as there is no such
            # field on the `Response` object.
            answer_texts = serializer.validated_data['answer_strings']
            del serializer.validated_data['answer_strings']

            # Create the empty response
            response = serializer.save(survey_id=self.kwargs['sid'])

            # Create a new `Answer` under this response for each answer_string
            # and question
            questions = response.survey.questions.all()
            for question, answer_text in zip(questions, answer_texts):
                response.answers.create(answer_text=answer_text,
                                        question=question)
        except DBError:
            raise exceptions.PermissionDenied

    @survey_context
    def get_queryset(self, survey): # pylint: disable=arguments-differ
        return survey.responses.all()


class ResponseDetail(generics.RetrieveDestroyAPIView):
    """ The view for an individual response

    Attributes:
        serializer_class      The serializer used for the objects in this view
        permission_classes    The required permissions to access this view
    """

    serializer_class = ResponseSerializer
    permission_classes = (permissions.IsAuthenticated,)

    @survey_context
    def get_object(self, survey): # pylint: disable=arguments-differ
        return survey.responses.all()[uri2ix(self, 'rid')]


class QuestionList(generics.ListCreateAPIView):
    """ The view for a list of questions. The queryset is limited to a specific
    survey.

    Attributes:
        serializer_class      The serializer used for the objects in this view
        permission_classes    The required permissions to access this view
    """

    serializer_class = QuestionSerializer
    permission_classes = (permissions.IsAuthenticated,)

    @survey_context
    def get_queryset(self, survey): # pylint: disable=arguments-differ
        return survey.questions.all()

    def perform_create(self, serializer):
        serializer.save(survey_id=self.kwargs['sid'])


class QuestionDetail(generics.RetrieveDestroyAPIView):
    """ The view for a single Question

    Attributes:
        serializer_class      The serializer used for the objects in this view
        permission_classes    The required permissions to access this view
    """

    serializer_class = QuestionSerializer
    permission_classes = (permissions.IsAuthenticated,)

    @survey_context
    def get_object(self, survey): # pylint: disable=arguments-differ
        return survey.questions.all()[uri2ix(self, 'qid')]

    # @@@ Question text needs to be put-able only ONCE, by the survey taker
    #     Only the survey owner can add tags


class AnswerList(generics.ListAPIView):
    """ The view for a list of answers (i.e. within an individual response).
    The queryset is limited to a specific response to a specific survey,
    as identified in the URI

    Attributes:
        serializer_class      The serializer used for the objects in this view
        permission_classes    The required permissions to access this view
    """

    serializer_class = AnswerSerializer
    permission_classes = (permissions.IsAuthenticated,)

    @survey_context
    def get_queryset(self, survey): # pylint: disable=arguments-differ
        return survey.responses.all()[uri2ix(self, 'rid')].answers.all()


# pylint: disable=too-many-ancestors
class AnswerDetail(generics.RetrieveUpdateDestroyAPIView):
    """ The view for a single answer

    Attributes:
        serializer_class      The serializer used for the objects in this view
        permission_classes    The required permissions to access this view
    """

    serializer_class = AnswerSerializer
    permission_classes = (permissions.IsAuthenticated,)

    @survey_context
    def get_object(self, survey): # pylint: disable=arguments-differ
        return survey.responses.all()[
            uri2ix(self, 'rid')].answers.all()[uri2ix(self, 'aid')]


class TagList(generics.ListCreateAPIView):
    """ The view for a set of tags. The queryset is limited to a specific
    Survey (identified by the URI)

    Attributes:
        serializer_class      The serializer used for the objects in this view
        permission_classes    The required permissions to access this view
    """

    serializer_class = TagSerializer
    permission_classes = (permissions.IsAuthenticated,)

    @survey_context
    def get_queryset(self, survey): # pylint: disable=arguments-differ
        return survey.tag_options.all()

    def perform_create(self, serializer):
        if not Tag.objects.filter(
                tag_text=serializer.validated_data["tag_text"]).exists():
            serializer.save(survey_id=self.kwargs["sid"])


# pylint: disable=too-many-ancestors
class TagDetail(generics.RetrieveUpdateDestroyAPIView):
    """ The view for a single tag

    Attributes:
        serializer_class      The serializer used for the objects in this view
        permission_classes    The required permissions to access this view
    """

    serializer_class = TagSerializer
    permission_classes = (permissions.IsAuthenticated,)

    @survey_context
    def get_object(self, survey): # pylint: disable=arguments-differ
        return survey.tag_options.all()[uri2ix(self, 'tid')]


class Register(FormView):
    """ The registration page/form.

    Attributes:
        template_name    The HTML template to format this view
        form_class       The form this page administers
        success_url      The landing page on successful registration
    """
    template_name = 'register.html'
    form_class = UserCreationForm
    success_url = '/surveys'

    def form_valid(self, form):
        """
        Do the needful when a valid form is submitted.
        """
        # Save the new user first
        form.save()
        # Get the username and password
        username = self.request.POST['username']
        password = self.request.POST['password1']
        # Authenticate user then login
        user = authenticate(username=username, password=password)
        login(self.request, user)
        return super(Register, self).form_valid(form)

