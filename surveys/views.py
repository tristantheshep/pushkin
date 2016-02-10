
from surveys.models import Survey, Response, Question, Answer, Tag
from surveys.serializers import SurveySerializer, ResponseSerializer, QuestionSerializer, UserSerializer, AnswerSerializer, TagSerializer
from surveys.permissions import affirm_survey_ownership

from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core import exceptions
from django.http import Http404
from django.views.generic import FormView
from rest_framework import generics
from rest_framework import permissions


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
        try:
            survey = Survey.objects.get(id=view.kwargs['sid'], owner=view.request.user)
            return func(view, survey)
        except Survey.DoesNotExist:
            raise exceptions.PermissionDenied
        except IndexError:
            raise Http404

    return query_wrapper


def uri2ix(view, key):
    """
    Maps an ordinal number string from a URI to an actual index.

    Example:- /surveys/<id>/responses/1 translates to "get the first response
              for survey with ID <id>", which translates into Python as
              survey.responses.all()[0]
    """
    return int(view.kwargs[key]) - 1


class SurveyList(generics.ListCreateAPIView):
    serializer_class = SurveySerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return Survey.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class SurveyDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = SurveySerializer
    permission_classes = (permissions.IsAuthenticated,)
    lookup_field = 'sid'

    @survey_context
    def get_object(self, survey):
        return survey


class ResponseList(generics.ListCreateAPIView):
    serializer_class = ResponseSerializer
    permission_classes = (permissions.IsAuthenticated,)

    @affirm_survey_ownership
    def perform_create(self, serializer):
        serializer.save(survey_id=self.kwargs['sid'])

    @survey_context
    def get_queryset(self, survey):
        return survey.responses.all()


class ResponseDetail(generics.RetrieveDestroyAPIView):
    serializer_class = ResponseSerializer
    permission_classes = (permissions.IsAuthenticated,)
    lookup_field = 'rid'

    @survey_context
    def get_object(self, survey):
        return survey.responses.all()[uri2ix(self, 'rid')]


class QuestionList(generics.ListCreateAPIView):
    serializer_class = QuestionSerializer
    permission_classes = (permissions.IsAuthenticated,)

    @survey_context
    def get_queryset(self, survey):
        return survey.questions.all()

    @affirm_survey_ownership
    def perform_create(self, serializer):
        serializer.save(survey_id=self.kwargs['sid'])


class QuestionDetail(generics.RetrieveDestroyAPIView):
    serializer_class = QuestionSerializer
    permission_classes = (permissions.IsAuthenticated,)
    lookup_field = 'qid'

    @survey_context
    def get_object(self, survey):
        return survey.questions.all()[uri2ix(self, 'qid')]

    # @@@ Question text needs to be put-able only ONCE, by the survey taker
    #     Only the survey owner can add tags


class AnswerList(generics.ListAPIView):
    serializer_class = AnswerSerializer
    permission_classes = (permissions.IsAuthenticated,)

    @survey_context
    def get_queryset(self, survey):
        return survey.responses.all()[uri2ix(self, 'rid')].answers.all()


class AnswerDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = AnswerSerializer
    permission_classes = (permissions.IsAuthenticated,)
    lookup_field = 'aid'

    @survey_context
    def get_object(self, survey):
        return survey.responses.all()[uri2ix(self, 'rid')].answers.all()[uri2ix(self, 'aid')]


class TagList(generics.ListCreateAPIView):
    serializer_class = TagSerializer
    permission_classes = (permissions.IsAuthenticated,)

    @survey_context
    def get_queryset(self, survey):
        return survey.tag_options.all()

    @affirm_survey_ownership
    def perform_create(self, serializer):
        if not Tag.objects.filter(tag_text=serializer.validated_data["tag_text"]).exists():
            serializer.save(survey_id=self.kwargs["sid"])


class TagDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TagSerializer
    permission_classes = (permissions.IsAuthenticated,)
    lookup_field = 'tid'

    @survey_context
    def get_object(self, survey):
        return survey.tag_options.all()[uri2ix(self, 'tid')]


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class Register(FormView):
   template_name = 'register.html'
   form_class = UserCreationForm
   success_url='/surveys'

   def form_valid(self, form):
      #save the new user first
      form.save()
      #get the username and password
      username = self.request.POST['username']
      password = self.request.POST['password1']
      #authenticate user then login
      user = authenticate(username=username, password=password)
      login(self.request, user)
      return super(Register, self).form_valid(form)

