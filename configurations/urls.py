from django.urls import path

from . import views
from configurations.ListViews import (
    TeamListView,
    SeriesListView,
    ChoiceListView,
    QuestionListView,
    )
from configurations.DetailViews import (
    TeamDetailView,
    SeriesDetailView,
    ChoiceDetailView,
    QuestionDetailView,
    )
from configurations.UpdateViews import (
    TeamUpdateView,
    SeriesUpdateView,
    ChoiceUpdateView,
    QuestionUpdateView,
    )
from configurations.CreateViews import (
    TeamCreateView,
    SeriesCreateView,
    ChoiceCreateView,
    QuestionCreateView,
    )

from django.conf.urls import url
app_name='configurations'

urlpatterns = [
    path('', views.index, name='homepage'),
    path('logout',views.logout_view,name='logout'),
    path('login',views.login_view,name='login'),
    path('registerUser',views.user_registration_view,name='register_user'),
    path('teams',TeamListView.as_view(),name='team_list_view'),
    path('configurations',views.configurations_home,name='configurations_home'),
    url(r'^team_view/(?P<obj_pk>\d+)$',TeamDetailView.as_view(),name='team_detail_view'),
    url(r'^team_update_view/(?P<obj_pk>\d+)$',TeamUpdateView.as_view(),name='team_update_view'),
    path('teams/create',TeamCreateView.as_view(),name='team_create_view'),
    path('series',SeriesListView.as_view(),name='series_list_view'),
    url(r'^series_view/(?P<obj_pk>\d+)$',SeriesDetailView.as_view(),name='series_detail_view'),
    url(r'^series_update_view/(?P<obj_pk>\d+)$',SeriesUpdateView.as_view(),name='series_update_view'),
    path('series/create',SeriesCreateView.as_view(),name='series_create_view'),
    path('choice',ChoiceListView.as_view(),name='choice_list_view'),
    url(r'^choice_view/(?P<obj_pk>\d+)$',ChoiceDetailView.as_view(),name='choice_detail_view'),
    url(r'^choice_update_view/(?P<obj_pk>\d+)$',ChoiceUpdateView.as_view(),name='choice_update_view'),
    path('choice/create',ChoiceCreateView.as_view(),name='choice_create_view'),
    path('question',QuestionListView.as_view(),name='question_list_view'),
    url(r'^question_view/(?P<obj_pk>\d+)$',QuestionDetailView.as_view(),name='question_detail_view'),
    url(r'^question_update_view/(?P<obj_pk>\d+)$',QuestionUpdateView.as_view(),name='question_update_view'),
    path('question/create',QuestionCreateView.as_view(),name='question_create_view'),
    path('ajax/choices_for_questions',views.choices_dependent_region,name='ajax_choices_for_questions'),
    
]