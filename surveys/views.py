
from surveys.models import Survey, SurveyResponse, Question, Answer, Tag
from surveys.serializers import SurveySerializer, SurveyResponseSerializer, QuestionSerializer, UserSerializer, AnswerSerializer, TagSerializer
from surveys.permissions import IsOwner

from django.conf import settings
from django.contrib.auth.models import User
from django.http import Http404
from django.shortcuts import redirect
from rest_framework import generics
from rest_framework import mixins
from rest_framework import permissions
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView


class SurveyList(generics.ListCreateAPIView):
    serializer_class = SurveySerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return Survey.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class SurveyDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = SurveySerializer
    queryset = Survey.objects.all()


class SurveyResponseList(generics.ListCreateAPIView):
    serializer_class = SurveyResponseSerializer

    def get_queryset(self):
        return SurveyResponse.objects.filter(survey_id=self.kwargs['sid'])

    def perform_create(self, serializer):
        serializer.save(survey_id=self.kwargs['sid'])


class SurveyResponseDetail(generics.RetrieveDestroyAPIView):
    serializer_class = SurveyResponseSerializer
    queryset = SurveyResponse.objects.all()


class QuestionList(generics.ListCreateAPIView):
    serializer_class = QuestionSerializer

    def get_queryset(self):
        return Question.objects.filter(survey_id=self.kwargs['sid'])

    def perform_create(self, serializer):
        serializer.save(survey_id=self.kwargs['sid'])


class QuestionDetail(generics.RetrieveDestroyAPIView):
    serializer_class = QuestionSerializer
    queryset = Question.objects.all()

    # @@@ Question text needs to be put-able only ONCE, by the survey taker
    #     Only the survey owner can add tags


class AnswerList(generics.ListAPIView):
    serializer_class = AnswerSerializer
    
    def get_queryset(self):
        return Answer.objects.filter(response_id=self.kwargs['rid'])


class AnswerDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = AnswerSerializer
    queryset = Answer.objects.all()


class TagList(generics.ListCreateAPIView):
    serializer_class = TagSerializer

    def get_queryset(self):
        return Tag.objects.filter(survey_id=self.kwargs["sid"])

    def perform_create(self, serializer):
        if not Tag.objects.filter(tag_text=serializer.validated_data["tag_text"]).exists():
            serializer.save(survey_id=self.kwargs["sid"])

class TagDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TagSerializer
    queryset = Tag.objects.all()


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

