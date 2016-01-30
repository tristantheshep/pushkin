from django.contrib import admin

from .models import Survey, Question, SurveyResponse, Answer
from django.forms import TextInput, Textarea
from django.db import models

class QuestionInline(admin.TabularInline):
    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows':1, 'columns':80})},
    }
    readonly_fields=('id',)
    extra = 0
    model = Question

class AnswerInline(admin.TabularInline):
    model = Answer

class SurveyResponseInline(admin.TabularInline):
    model = SurveyResponse
    inlines = [
        AnswerInline,
    ]

class SurveyAdmin(admin.ModelAdmin):
    search_fields = ['name']
    inlines = [
        QuestionInline,
        SurveyResponseInline,
    ]


admin.site.register(Survey, SurveyAdmin)
