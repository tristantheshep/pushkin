
""" Serialization definitions for the models in this app """

from rest_framework import serializers

from .models import Survey, Response, Question, Answer, Tag


class TagSerializer(serializers.ModelSerializer):
    """ Serialization definition for the `Tag` object.

    Tags are serialized as:
        {
            'tag_text' : <tag_text>
        }
    """
    class Meta:
        model = Tag
        fields = ('tag_text',)

class AnswerSerializer(serializers.ModelSerializer):
    """ Serialization definition for the `Answer` object.

    Answers are serialized as:
        {
            'answer_text' : <answer_text>,
            'tags' : [<tag_text>, <tag_text>, ...]
        }
    """

    class Meta:
        model = Answer
        fields = ('answer_text', 'tags',)

class ResponseSerializer(serializers.ModelSerializer):
    """ Serialization definition for the the `Response` objects

    Responses are serialized as:
        {
            'answers' : [<answer_text>, <answer_text>, ...]
        }
    """
    # Specify the answers as a SlugRelatedField to provide a 'shortcut' i.e.
    # when a Response is serialized, it simply specifies a list of strings
    # rather than a list of entire `AnswerSerializers`, each containing the
    # redundant "answer_text" key.
    answers = serializers.SlugRelatedField(many=True,
                                           slug_field='answer_text',
                                           read_only=True)

    class Meta:
        model = Response
        fields = ('answers',)
        read_only_fields = ('answers',)

class QuestionSerializer(serializers.ModelSerializer):
    """ Serialization definition for the the `Question` objects

    Questions are serialized as:
        {
            'question_text' : <question_text>
        }
    """
    class Meta:
        model = Question
        fields = ('question_text',)

class SurveySerializer(serializers.ModelSerializer):
    """ Serialization definition for the the `Survey` object

    Responses are serialized as:
        {
            'questions' : [<question_text>, <question_text>, ...],
            'tag_options' : [<tag_text>, <tag_text>, ...],
            'id' : <id>,
            'name' : <name>,
            'response_count' : <number of associated `Response` objects>,
            'published' : <True|False>
        }

    """
    # Use SlugRelatedFields for questions and tags rather than the entire
    # respective serializers
    questions = serializers.SlugRelatedField(many=True,
                                             slug_field='question_text',
                                             read_only=True)
    tag_options = serializers.SlugRelatedField(many=True,
                                               slug_field='tag_text',
                                               read_only=True)

    def validate(self, data):
        """ Prevent the `published` variable being set to False """ 
        if 'published' in data and data.get('published') == False:
            del data['published']
        return data

    class Meta:
        model = Survey
        fields = ('id', 'name', 'questions', 'tag_options', 'response_count',
                  'published')

