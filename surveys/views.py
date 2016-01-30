from surveys.models import Survey, SurveyResponse, Question, Answer
from surveys.serializers import SurveySerializer, SurveyResponseSerializer, QuestionSerializer, UserSerializer, AnswerSerializer
from surveys.permissions import IsOwnerOrReadOnly

from django.contrib.auth.models import User
from django.http import Http404
from rest_framework import generics
from rest_framework import mixins
from rest_framework import permissions
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

class SurveyList(generics.ListCreateAPIView):
    queryset = Survey.objects.all()
    serializer_class = SurveySerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class SurveyDetail(APIView):

    def get_survey(self, pk):
        try:
            return Survey.objects.get(pk=pk)
        except Survey.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        survey = self.get_survey(pk)
        serializer = SurveySerializer(survey)
        return Response(serializer.data)

    def patch(self,  request, pk, format=None):

        survey = self.get_survey(pk)
        serializer = SurveySerializer(survey, request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.data, status=status.HTTP_200_OK)


class SurveyResponseList(APIView):

    def get(self, request, sid, format=None):
        responses = SurveyResponse.objects.filter(survey_id=sid)
        serializer = SurveyResponseSerializer(responses, many=True)
        return Response(serializer.data)

    def post(self, request, sid, format=None):
       serializer = SurveyResponseSerializer(data=request.data)
       if serializer.is_valid():
           serializer.save(survey_id=sid)
           return Response(serializer.data, status=status.HTTP_201_CREATED)
       return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

 
class SurveyResponseDetail(APIView):

    def get_survey_response(self, sid, rid):
        try:
            return SurveyResponse.objects.get(survey_id=sid, id=rid)
        except SurveyResponse.DoesNotExist:
            raise Http404

    def get(self, request, format=None, sid=None, rid=None):
        response = self.get_survey_response(sid, rid)
        serializer = SurveyResponseSerializer(response)
        return Response(serializer.data)

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

class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
