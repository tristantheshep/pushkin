from django.db import models

MAX_TAG_LENGTH = 20

class Survey(models.Model):
    """
    The root of each survey
    """
    name = models.CharField(max_length=101)
    created = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey('auth.user', related_name='surveys')
    
    class Meta:
        ordering = ('created',)

    def __str__(self):
        return self.name

class Question(models.Model):
    """
    An individual question beloning to a survey
    """
    survey = models.ForeignKey(Survey, related_name='questions')
    question_text = models.TextField()

    def __str__(self):
        return self.question_text

class TagChoice(models.Model):
    """
    A tag that the survey owner can use to tag responses in the survey 
    """
    tag_text = models.CharField(max_length=MAX_TAG_LENGTH)
    survey = models.ForeignKey(Survey, related_name='tag_options')

    def __str__(self):
        return self.tag_text

class SurveyResponse(models.Model):
    """
    A series of answers representing a response to the survey
    """
    survey = models.ForeignKey(Survey, related_name='responses')

class Answer(models.Model):
    """
    A single answer to a question that comprises the survey
    """
    response = models.ForeignKey(SurveyResponse, related_name='answers')
    answer_text = models.TextField()

    def __str__(self):
        return self.answer_text[:10] + "..."

class Tag(models.Model):
    """
    A single tag attached to a single answer
    """
    answer = models.ForeignKey(Answer, related_name='tags')
    text = models.CharField(max_length=MAX_TAG_LENGTH)
