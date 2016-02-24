
""" The various views for the survey URLs """

from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.core import exceptions
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.views.generic import FormView
from rest_framework import generics
from rest_framework import permissions

from .models import Survey, Tag
from .serializers import (SurveySerializer, ResponseSerializer,
                          QuestionSerializer, AnswerSerializer, TagSerializer)


################################################################################
# UI/response submission handlers
#

def respond(request, sid):
    """ Renders the landing page for a user taking a survey """
    survey = get_object_or_404(Survey, id=sid)
    return render(request, 'surveys/respond.html', {'survey':survey})

def submit(request, sid):
    """ Processes the response to the survey as rendered by `respond()` """
    response_values = request.POST
    survey = get_object_or_404(Survey, id=sid)
    questions = survey.questions.all()
    response = survey.responses.create()
    for question in questions:
        response.answers.create(
            question=question,
            answer_text=response_values[question.question_text])

    return HttpResponseRedirect('/thankyou/')

def thankyou(request):
    """ Thank-you page after submitting a survey response """
    return render(request, 'surveys/thankyou.html')


################################################################################
# Backend/RESTful handlers
#

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


class ResponseList(generics.ListAPIView):
    """ The view for survey's list of responses. The queryset is limited
    to a specific survey, as identified in the URI

    Attributes:
        serializer_class      The serializer used for the objects in this view
        permission_classes    The required permissions to access this view
    """

    serializer_class = ResponseSerializer
    permission_classes = (permissions.IsAuthenticated,)

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

    def perform_update(self, serializer):
        tag_strings = serializer.validated_data.pop('tag_strings', [])
        answer = serializer.save()
        tags = Tag.objects.filter(tag_text__in=tag_strings)
        for tag in tags:
            answer.tags.add(tag)
        answer.save()

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

