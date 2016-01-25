from django.db import models

class Survey(models.Model):
    """
    The root of each survey
    """
    name = models.CharField(max_length=101)
    created = models.DateTimeField(auto_now_add=True)
    
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

class TagChoice(models.Model):
    """
    A tag that the survey owner can use to tag responses in the survey 
    """
    tag_text = models.CharField(max_length=20)
    survey = models.ForeignKey(Survey, related_name='tag_options')

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

class Tag(models.Model):
    """
    A single tag attached to a single answer
    """
    answer = models.ForeignKey(Answer, related_name='tags')
