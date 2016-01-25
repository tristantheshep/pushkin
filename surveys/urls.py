from surveys import views

from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    url(r'^surveys/$', views.SurveyList.as_view()),
    url(r'^surveys/(?P<pk>[0-9]+)/$', views.SurveyDetail.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
