from rest_framework import serializers
from surveys.models import Survey, TagChoice, Question, Tag

class TagChoiceSerializer(serializers.Serializer):
    tag_text = serializers.CharField(max_length=100)

    def create(self, validated_data):
        """
        Create a new tag from validated data
        """
        return TagChoice.objects.create(**validated_data)

    def update(self, validated_data):
        instance.tag_text = validated_data.get('tag_text', instance.tag_text)

class TagSerializer(serializers.Serializer):
    tag_choice = TagChoiceSerializer()

    def create(self, validated_data):
        """
        Add a tag to a question
        """
        return Tag.objects.create(**validated_data)

class AnswerSerializer(serializers.Serializer):
    text_answer = serializers.CharField(max_length=500)
    tags = TagSerializer(many=True)

    # Note - create/update ommitted intentionally.

class SurveyResponseSerializer(serializers.Serializer):
    answers = AnswerSerializer(many=True)
    
    # Note - create/update ommitted intentionally.

class QuestionSerializer(serializers.Serializer):
    question_text = serializers.CharField(max_length=100)

    def create(self, validated_data):
        """
        Create and return a new `Question` instance from validated data
        """
        return Question.objects.create(**validated_data)

    # Note - update() method intentionally left out.


class SurveySerializer(serializers.Serializer):
    pk = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=100)
    questions = QuestionSerializer(many=True)
    tag_options = TagChoiceSerializer(many=True)
    responses = SurveyResponseSerializer(many=True)

    def create(self, validated_data):
        """
        Create and return a new `Survey` instance, given the validated data.
        """
        return Survey.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing `Survey` instance, given the validated data
        """
        instance.name = validated_data.get('name', instance.name)
        instance.questions = validated_data.get('questions', instance.questions)
        instance.tag_options = validate_data.get('tag_options', instance.tag_options)
        instance.save()
