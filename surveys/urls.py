from surveys import views

from django.conf.urls import include
from django.conf.urls import url
from django.contrib.auth.forms import UserCreationForm
from django.views.generic.edit import CreateView
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
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
    url('^register/', CreateView.as_view(template_name='register.html',
                                         form_class=UserCreationForm,
                                         success_url='/'), name='register'),
    url(r'^api-auth/', include('rest_framework.urls',
                               namespace='rest_framework')),
    url(r'^users/$', views.UserList.as_view()),
    url(r'^users/(?P<pk>[0-9]+)/$', views.UserDetail.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
