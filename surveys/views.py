
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

def get_survey(sid, user):
    return Survey.objects.get(id=sid, owner=user)


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

    def get_queryset(self):
        return Survey.objects.filter(owner=self.request.user)


class ResponseList(generics.ListCreateAPIView):
    serializer_class = ResponseSerializer
    permission_classes = (permissions.IsAuthenticated,)

    @affirm_survey_ownership
    def perform_create(self, serializer):
        serializer.save(survey_id=self.kwargs['sid'])

    def get_queryset(self):
        survey = get_survey(self.kwargs['sid'], self.request.user)
        return survey.responses.all()


class ResponseDetail(generics.RetrieveDestroyAPIView):
    serializer_class = ResponseSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        sid = self.kwargs['sid']
        user = self.request.user
        responseIx = int(self.kwargs['pk']) - 1
        try:
            return get_survey(sid, user).responses.all()[responseIx]
        except IndexError:
            raise Http404


class QuestionList(generics.ListCreateAPIView):
    serializer_class = QuestionSerializer
    permission_classes = (permissions.IsAuthenticated,)
    
    def get_queryset(self):
        sid = self.kwargs['sid']
        user = self.request.user
        try:
            return get_survey(sid, user).questions.all()
        except IndexError:
            raise Http404

    @affirm_survey_ownership
    def perform_create(self, serializer):
        serializer.save(survey_id=self.kwargs['sid'])


class QuestionDetail(generics.RetrieveDestroyAPIView):
    serializer_class = QuestionSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        sid = self.kwargs['sid']
        user = self.request.user
        questionIx = int(self.kwargs['pk']) - 1
        try:
            return get_survey(sid, user).questions.all()[questionIx]
        except IndexError:
            raise Http404

    # @@@ Question text needs to be put-able only ONCE, by the survey taker
    #     Only the survey owner can add tags


class AnswerList(generics.ListAPIView):
    serializer_class = AnswerSerializer
    permission_classes = (permissions.IsAuthenticated,)
    
    def get_queryset(self):
        sid = self.kwargs['sid']
        responseIx = int(self.kwargs['rid']) - 1
        user = self.request.user
        try:
            return get_survey(sid, user).responses.all()[responseIx].answers.all()
        except IndexError:
            raise Http404


class AnswerDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = AnswerSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        sid = self.kwargs['sid']
        responseIx = int(self.kwargs['rid']) - 1
        answerIx = int(self.kwargs['pk']) - 1
        user = self.request.user
        try:
            return get_survey(sid, user).responses.all()[responseIx].answers.all()[answerIx]
        except IndexError:
            raise Http404


class TagList(generics.ListCreateAPIView):
    serializer_class = TagSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        sid = self.kwargs['sid']
        user = self.request.user
        try:
            return get_survey(sid, user).tags.all()
        except IndexError:
            raise Http404

    @affirm_survey_ownership
    def perform_create(self, serializer):
        if not Tag.objects.filter(tag_text=serializer.validated_data["tag_text"]).exists():
            serializer.save(survey_id=self.kwargs["sid"])


class TagDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TagSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        sid = self.kwargs['sid']
        tagIx = int(self.kwargs['pk']) - 1
        user = self.request.user
        try:
            return get_survey(sid, user).tags.all()[tagIx]
        except IndexError:
            raise Http404


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

