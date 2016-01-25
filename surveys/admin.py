from django.contrib import admin

from .models import Survey, Question, TagChoice, SurveyResponse, Answer
from django.forms import TextInput, Textarea
from django.db import models

class BaseDefaults:
    readonly_fields=('id',)
    extra = 0

class QuestionInline(admin.TabularInline, BaseDefaults):
    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows':1, 'columns':80})},
    }
    model = Question

class TagChoiceInline(admin.TabularInline, BaseDefaults):
    model = TagChoice

class AnswerInline(admin.TabularInline, BaseDefaults):
    model = Answer

class SurveyReponseInline(admin.TabularInline, BaseDefaults):
    model = SurveyResponse
    inlines = [
        AnswerInline,
    ]

class SurveyAdmin(admin.ModelAdmin, BaseDefaults):
    search_fields = ['name']
    inlines = [
        QuestionInline,
        TagChoiceInline,
    ]


admin.site.register(Survey, SurveyAdmin)
#admin.site.register(Question, QuestionAdmin)
