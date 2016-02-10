from rest_framework import serializers

from surveys.models import Survey, Response, Question, Answer, Tag

import json

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('tag_text',)

class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ('answer_text', 'tags',)

class ResponseSerializer(serializers.ModelSerializer):
    answers = serializers.SlugRelatedField(many=True,
                                           slug_field='answer_text',
                                           read_only=True)

    class Meta:
        model = Response
        fields = ('answers',)
        read_only_fields = ('answers',)

class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ('question_text',)        

class SurveySerializer(serializers.ModelSerializer):
    questions = serializers.SlugRelatedField(many=True,
                                             slug_field='question_text',
                                             read_only=True)
    tag_options = serializers.SlugRelatedField(many=True,
                                               slug_field='tag_text',
                                               read_only=True)
    class Meta:
        model = Survey
        fields = ('id', 'name', 'questions', 'tag_options', 'response_count',
                  'published')

