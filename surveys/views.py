
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


class QuestionList(APIView):

    def get(self, request, format=None, sid=None):
        questions = Question.objects.filter(survey_id=sid)
        serializer = QuestionSerializer(questions, many=True)
        return Response(serializer.data)

    def post(self, request, format=None, sid=None):
       survey = Survey.objects.get(pk=sid)
       serializer = QuestionSerializer(data=request.data, partial=True)
       if serializer.is_valid():
           serializer.save(survey_id=sid)
           return Response(serializer.data, status=status.HTTP_201_CREATED)
       return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class QuestionDetail(APIView):

    def get(self, request, format=None, sid=None, qid=None):
        question = Question.objects.get(survey_id=sid, id=qid)
        serializer = QuestionSerializer(question)
        return Response(serializer.data)


class AnswerList(APIView):

    def get(self, request, sid, rid, format=None):
        answers = Answer.objects.filter(response_id=rid)
        serializer = AnswerSerializer(answers, many=True)
        return Response(serializer.data)

    def post(self, request, sid, rid, format=None):
        response = SurveyResponse.objects.get(pk=rid)
        serializer = AnswerSerializer(data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save(response_id=rid)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AnswerDetail(APIView):

    def get_answer(self, rid, aid):
        try:
            return Answer.objects.get(response_id=rid, pk=aid)    
        except:
            raise Http404

    def get(self, request, sid, rid, aid, format=None):
        answer = self.get_answer(rid, aid)
        serializer = AnswerSerializer(answer)
        return Response(serializer.data)

    def patch(self, request, sid, rid, aid, format=None):
        answer = self.get_answer(rid, sid)
        serializer = AnswerSerializer(answer, request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.data, status=status.HTTP_200_OK)

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

