
from surveys.models import Survey, Response, Question, Answer, Tag
from surveys.serializers import SurveySerializer, ResponseSerializer, QuestionSerializer, UserSerializer, AnswerSerializer, TagSerializer
from surveys.permissions import IsOwner, affirm_survey_ownership

from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
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
              equivalent of  Surveys.get(pk=<survey_id>).responses.all().

    The decorator also catches any IndexErrors to raise a 404 if necessary.

    Example:- if only 3 responses exist under a survey, then accessing 
              /survey/<id>/responses/4 will result in an indexerror as
              ResponseDetail.get_object() will assume survey.responses.all()[3]
              to exist.
    """

    def query_wrapper(view):
        try:
            survey = Survey.objects.get(id=view.kwargs['sid'], owner=view.request.user)
            return func(view, survey)
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

    @survey_context
    def get_queryset(self):
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

    @survey_context
    def get_object(self, survey):
        return survey.responses.all()[uri2ix(self, 'pk')]


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

    @survey_context
    def get_object(self):
        return survey.questions.all()[uri2ix(self, 'pk')]

    # @@@ Question text needs to be put-able only ONCE, by the survey taker
    #     Only the survey owner can add tags


class AnswerList(generics.ListAPIView):
    serializer_class = AnswerSerializer
    permission_classes = (permissions.IsAuthenticated,)

    @survey_context
    def get_queryset(self):
        return survey.responses.all()[uri2ix(self, 'rid')].answers.all()


class AnswerDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = AnswerSerializer
    permission_classes = (permissions.IsAuthenticated,)

    @survey_context
    def get_object(self):
        return survey.responses.all()[uri2ix(self, 'rid')].answers.all()[uri2ix(self, 'pk')]


class TagList(generics.ListCreateAPIView):
    serializer_class = TagSerializer
    permission_classes = (permissions.IsAuthenticated,)

    @survey_context
    def get_queryset(self):
        return survey.tags.all()

    @affirm_survey_ownership
    def perform_create(self, serializer):
        if not Tag.objects.filter(tag_text=serializer.validated_data["tag_text"]).exists():
            serializer.save(survey_id=self.kwargs["sid"])


class TagDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TagSerializer
    permission_classes = (permissions.IsAuthenticated,)

    @survey_context
    def get_object(self):
        return survey.tags.all()[uri2ix(self, 'pk')]


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

