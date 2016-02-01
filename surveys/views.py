
from surveys.models import Survey, Response, Question, Answer, Tag
from surveys.serializers import SurveySerializer, ResponseSerializer, QuestionSerializer, UserSerializer, AnswerSerializer, TagSerializer
from surveys.permissions import IsOwner, affirm_survey_ownership

from django.contrib.auth.models import User
from rest_framework import generics
from rest_framework import permissions


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

    @affirm_survey_ownership
    def get_queryset(self):
        return Response.objects.filter(survey_id=self.kwargs['sid'])


class ResponseDetail(generics.RetrieveDestroyAPIView):
    serializer_class = ResponseSerializer
    permission_classes = (permissions.IsAuthenticated,)

    @affirm_survey_ownership
    def get_queryset(self):
        return Response.objects.all() 


class QuestionList(generics.ListCreateAPIView):
    serializer_class = QuestionSerializer
    permission_classes = (permissions.IsAuthenticated,)
    
    @affirm_survey_ownership
    def get_queryset(self):
        return Question.objects.filter(survey_id=self.kwargs['sid'])

    @affirm_survey_ownership
    def perform_create(self, serializer):
        serializer.save(survey_id=self.kwargs['sid'])


class QuestionDetail(generics.RetrieveDestroyAPIView):
    serializer_class = QuestionSerializer
    permission_classes = (permissions.IsAuthenticated,)

    @affirm_survey_ownership
    def get_queryset(self):
        return Question.objects.all()

    # @@@ Question text needs to be put-able only ONCE, by the survey taker
    #     Only the survey owner can add tags


class AnswerList(generics.ListAPIView):
    serializer_class = AnswerSerializer
    permission_classes = (permissions.IsAuthenticated,)
    
    @affirm_survey_ownership
    def get_queryset(self):
        return Answer.objects.filter(response_id=self.kwargs['rid'])


class AnswerDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = AnswerSerializer
    permission_classes = (permissions.IsAuthenticated,)

    @affirm_survey_ownership
    def get_queryset(self):
        return Answer.objects.filter(response_id=self.kwargs['rid'])


class TagList(generics.ListCreateAPIView):
    serializer_class = TagSerializer
    permission_classes = (permissions.IsAuthenticated,)

    @affirm_survey_ownership
    def get_queryset(self):
        return Tag.objects.filter(survey_id=self.kwargs["sid"])

    @affirm_survey_ownership
    def perform_create(self, serializer):
        if not Tag.objects.filter(tag_text=serializer.validated_data["tag_text"]).exists():
            serializer.save(survey_id=self.kwargs["sid"])


class TagDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TagSerializer
    permission_classes = (permissions.IsAuthenticated,)

    @affirm_survey_ownership
    def get_queryset(self):
        return Tag.objects.all()


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

