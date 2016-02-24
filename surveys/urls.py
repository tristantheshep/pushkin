
""" URL-to-view definitions for this app """

from django.conf.urls import include
from django.conf.urls import url
from django.views.generic import RedirectView
from rest_framework.urlpatterns import format_suffix_patterns

from . import views


urlpatterns = [
    url(r'^$', RedirectView.as_view(url='/surveys/', permanent=True)),
    url(r'^surveys/$', views.SurveyList.as_view()),
    url(r'^surveys/(?P<sid>[0-9]+)/$', views.SurveyDetail.as_view()),
    url(r'^surveys/(?P<sid>[0-9]+)/questions/$', views.QuestionList.as_view()),
    url(r'^surveys/(?P<sid>[0-9]+)/questions/(?P<qid>[0-9]+)/$',
        views.QuestionDetail.as_view()),
    url(r'^surveys/(?P<sid>[0-9]+)/responses/$',
        views.ResponseList.as_view()),
    url(r'^surveys/(?P<sid>[0-9]+)/responses/(?P<rid>[0-9]+)/$',
        views.ResponseDetail.as_view()),
    url(r'^surveys/(?P<sid>[0-9]+)/responses/(?P<rid>[0-9]+)/answers/$',
        views.AnswerList.as_view()),
    url((r'^surveys/(?P<sid>[0-9]+)/responses/(?P<rid>[0-9]+)/answers/'
         r'(?P<aid>[0-9]+)/$'), views.AnswerDetail.as_view()),
    url(r'^surveys/(?P<sid>[0-9]+)/tags/$', views.TagList.as_view()),
    url(r'^surveys/(?P<sid>[0-9]+)/tags/(?P<tid>[0-9]+)/$',
        views.TagDetail.as_view()),
    url(r'^register/', views.Register.as_view(), name='register'),
    url(r'^api-auth/', include('rest_framework.urls',
                               namespace='rest_framework')),
    url(r'^respond/(?P<sid>[0-9]+)/$', views.respond, name='respond'),
    url(r'^submit/(?P<sid>[0-9]+)/$', views.submit, name='submit'),
    url(r'^thankyou/$', views.thankyou, name='thankyou'),
]

# Add on suffix pattern options, e.g. '.json' to each URL
urlpatterns = format_suffix_patterns(urlpatterns)
