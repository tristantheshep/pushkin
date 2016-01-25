from django.contrib import admin

from .models import Survey, Question, TagChoice, SurveyResponse, Answer
from django.forms import TextInput, Textarea
from django.db import models

class QuestionInline(admin.TabularInline):
    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows':1, 'columns':80})},
    }
    readonly_fields=('id',)
    extra = 0
    model = Question

class TagChoiceInline(admin.TabularInline):

    readonly_fields=('id',)
    extra = 0
    model = TagChoice

class AnswerInline(admin.TabularInline):
    model = Answer

class SurveyReponseInline(admin.TabularInline):
    model = SurveyResponse
    inlines = [
        AnswerInline,
    ]

class SurveyAdmin(admin.ModelAdmin):
    search_fields = ['name']
    inlines = [
        QuestionInline,
        TagChoiceInline,
    ]


admin.site.register(Survey, SurveyAdmin)
