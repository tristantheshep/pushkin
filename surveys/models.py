
""" The DB/model definitions for this application """

from django.conf import settings
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token


MAX_TAG_LENGTH = 100
"""
The maximum length of each tag text
"""


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
# pylint: disable=unused-argument
def create_auth_token(sender, instance=None, created=False, **kwargs):
    """ Automatically add an auth token to a newly create user """
    if created:
        Token.objects.create(user=instance)


class DBError(Exception):
    """ Exception thrown to indicate an attempted action has been rejected at
    the DB layer, i.e. responding to an unpublished survey or editing a
    question after publication
    """

class Survey(models.Model):
    """ The root object of each survey

    Attributes:
        name         The name of the survey, as specified by the survey owner
        create       A `DateTimeField` specifying when the survey was created
        owner        A `User` instance representing the creator of the survey
        published    Flags if the survey is open and accepting responses
    """
    name = models.CharField(max_length=100, default='My Survey')
    created = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey('auth.User', related_name='surveys')
    published = models.BooleanField(default=False)

    class Meta:
        """ Meta details to specify that the Surveys should be ordered
        chronoligically
        """
        ordering = ('created',)

    def publish(self):
        """ Alters a survey's state to published """
        self.published = True
        self.save()# pylint: disable=no-member

    @property
    def response_count(self):
        """ A `property` to export the number of responses, user when
        serializing a Survey
        """
        return self.responses.count()


class Question(models.Model):
    """ An individual question belonging to a survey

    Attributes:
        survey           The `Survey` object to which this question belongs
        question_text    The question string to display
    """
    survey = models.ForeignKey(Survey, related_name='questions')
    question_text = models.TextField()


class Tag(models.Model):
    """ A tag that the survey owner can use to tag responses in the survey

    Attributes:
        survey      The `Survey` object to which this tag belongs
        tag_text    The tag string to display
    """
    tag_text = models.CharField(max_length=MAX_TAG_LENGTH)
    survey = models.ForeignKey(Survey, related_name='tag_options')


class Response(models.Model):
    """ A series of answers representing a response to the survey

    Attributes:
        survey       The `Survey` object to which this response belongs
    """
    survey = models.ForeignKey(Survey, related_name='responses')

    @property
    def answer_strings(self):
        """ A property to mimic a list of answer texts for this response.
        Used so we can specify the `answer_strings` attribute in the
        corresponding serializer and have it seamlessly output just the
        text
         """
        return [answer.answer_text for answer in self.answers.all()]

    def save(self, *args, **kwargs):
        """ Saves the response if the survey is published, otherwise raises
        a DBError
         """
        if self.survey.published:
            # pylint: disable=no-member
            super(Response, self).save(*args, **kwargs)
        else:
            raise DBError('This survey has not been published')


class Answer(models.Model):
    """ A single answer to a question that composes the survey

    Attributes:
        response       The `Response` object that contains this answer
        question       The `Question` to which this is the answer for
        answer_text    The answer text, to be populated by a survey respondent
        tags           A series of tags associated with this answer, added by
                       the survey owner after completion
    """
    response = models.ForeignKey(Response, related_name='answers')
    question = models.ForeignKey(Question, related_name='answers')
    answer_text = models.TextField()
    tags = models.ManyToManyField(Tag, blank=True)

    @property
    def tag_strings(self):
        """ Returns the `tag_text` fields in a list for all tags associated
        with this answer
        """
        return [tag.tag_text for tag in self.tags.all()]
