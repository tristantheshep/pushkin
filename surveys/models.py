from django.conf import settings
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

MAX_TAG_LENGTH = 20


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


class Survey(models.Model):
    """
    The root of each survey
    """
    name = models.CharField(max_length=101)
    created = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey('auth.User', related_name='surveys')
    
    class Meta:
        ordering = ('created',)

    def __str__(self):
        return self.name

    @property
    def response_count(self):
        return self.responses.count() 

class Question(models.Model):
    """
    An individual question beloning to a survey
    """
    survey = models.ForeignKey(Survey, related_name='questions')
    question_text = models.TextField()

    def __str__(self):
        return self.question_text

class Tag(models.Model):
    """
    A tag that the survey owner can use to tag responses in the survey 
    """
    tag_text = models.CharField(max_length=MAX_TAG_LENGTH)
    survey = models.ForeignKey(Survey, related_name='tag_options')

    def __str__(self):
        return self.tag_text

class Response(models.Model):
    """
    A series of answers representing a response to the survey
    """
    survey = models.ForeignKey(Survey, related_name='responses')

    def save(self, *args, **kwargs):
        super(Response, self).save(*args, **kwargs)
        for question in self.survey.questions.all():
            self.answers.create(question_id=question.id)

class Answer(models.Model):
    """
    A single answer to a question that comprises the survey
    """
    response = models.ForeignKey(Response, related_name='answers')
    question = models.ForeignKey(Question, related_name='answers')
    answer_text = models.TextField()
    tags = models.ManyToManyField(Tag, blank=True)

    def __str__(self):
        return self.answer_text[:10] + "..."
