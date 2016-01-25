
from django.conf.urls import url
from surveys import views

urlpatterns = [
    url(r'^surveys/$', views.survey_list),
    url(r'^surveys/(?P<pk>[0-9]+)/$', views.survey_detail),
]
