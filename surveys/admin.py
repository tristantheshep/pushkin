
""" Admin definitions for this app """

from django.contrib import admin
from django.forms import Textarea
from django.db import models

from .models import Survey, Question, Response, Answer


class QuestionInline(admin.TabularInline):
    """ Inline admin definition for the `Question` model """
    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows':1, 'columns':80})},
    }
    readonly_fields = ('id',)
    extra = 0
    model = Question

class AnswerInline(admin.TabularInline):
    """ Inline admin definition for the `Answer` model """
    model = Answer

class ResponseInline(admin.TabularInline):
    """ Inline admin definition for the `Response` model """
    model = Response
    inlines = [
        AnswerInline,
    ]

class SurveyAdmin(admin.ModelAdmin):
    """ Admin model for the top-level `Survey` object

    Allows for searching by survey name and includes question and response
    inlines.
    """
    search_fields = ['name']
    inlines = [
        QuestionInline,
        ResponseInline,
    ]


admin.site.register(Survey, SurveyAdmin)
