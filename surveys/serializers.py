from django.contrib.auth.models import User
from rest_framework import serializers

from surveys.models import Survey, Response, Question, Answer, Tag

import json

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('tag_text', 'id')

class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ('answer_text', 'tags', 'id')

class ResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Response
        fields = ('answers','id')
        read_only_fields = ('answers','id')

class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ('question_text','id')        

class SurveySerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    class Meta:
        model = Survey
        fields = ('pk', 'name', 'questions', 'tag_options', 'owner', 'responses')

class UserSerializer(serializers.ModelSerializer):
    surveys = serializers.PrimaryKeyRelatedField(many=True, queryset=Survey.objects.all())

    class Meta:
        model = User
        fields = ('id', 'username', 'surveys')
