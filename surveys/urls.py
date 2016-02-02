from surveys import views

from django.conf.urls import include
from django.conf.urls import url
from django.views.generic import RedirectView
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    url(r'^$', RedirectView.as_view(url='/surveys/')),
    url(r'^surveys/$', views.SurveyList.as_view()),
    url(r'^surveys/(?P<pk>[0-9]+)/$', views.SurveyDetail.as_view()),
    url(r'^surveys/(?P<sid>[0-9]+)/questions/$', views.QuestionList.as_view()),
    url(r'^surveys/(?P<sid>[0-9]+)/questions/(?P<pk>[0-9]+)$', 
            views.QuestionDetail.as_view()),
    url(r'^surveys/(?P<sid>[0-9]+)/responses/$', 
            views.ResponseList.as_view()),
    url(r'^surveys/(?P<sid>[0-9]+)/responses/(?P<pk>[0-9]+)$', 
            views.ResponseDetail.as_view()),
    url(r'^surveys/(?P<sid>[0-9]+)/responses/(?P<rid>[0-9]+)/answers/$', 
            views.AnswerList.as_view()),
    url(r'^surveys/(?P<sid>[0-9]+)/responses/(?P<rid>[0-9]+)/answers/(?P<pk>[0-9]+)$', views.AnswerDetail.as_view()),
    url(r'^surveys/(?P<sid>[0-9]+)/tags/$', views.TagList.as_view()),
    url(r'^surveys/(?P<sid>[0-9]+)/tags/(?P<pk>[0-9]+)$',
            views.TagDetail.as_view()),
    url('^register/', views.Register.as_view(), name='register'),
    url(r'^api-auth/', include('rest_framework.urls',
                               namespace='rest_framework')),
    url(r'^users/$', views.UserList.as_view()),
    url(r'^users/(?P<pk>[0-9]+)/$', views.UserDetail.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
