from rest_framework import serializers
from surveys.models import Survey, SurveyResponse, TagChoice, Question, Answer, Tag

class TagChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = TagChoice
        fields = ('tag_text',)

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('tag_text',)

class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ('answer_text, tags')
        read_only_fields = ('answer_text')

class SurveyResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = SurveyResponse
        fields = ('answers',)
        read_only_fields = ('answers')

class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ('question_text',)        

class SurveySerializer(serializers.Serializer):
    pk = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=100)
    questions = QuestionSerializer(many=True)
    tag_options = TagChoiceSerializer(many=True)
#   responses = SurveyResponseSerializer(many=True)

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
