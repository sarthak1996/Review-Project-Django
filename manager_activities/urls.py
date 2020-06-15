from django.urls import path

from . import views
from django.conf.urls import url
from manager_activities.ListViews import(
		PeerReviewManagerListView,
		PeerTestingManagerListView
	)
from manager_activities.DetailViews import(
		PeerReviewManagerDetailView,
		PeerTestingManagerDetailView
	)

app_name='manager_activities'

urlpatterns =[
	path('manager_home',views.manager_view_landing_page,name='manager_home'),
	path('peer_review_manager_list',PeerReviewManagerListView.as_view(),name='peer_review_manager_list'),
	path('peer_testing_manager_list',PeerTestingManagerListView.as_view(),name='peer_testing_manager_list'),
	url(r'^manager_review_view/(?P<obj_pk>\d+)$',PeerReviewManagerDetailView.as_view(),name='manager_review_view'),
	url(r'^manager_peer_testing_view/(?P<obj_pk>\d+)$',PeerTestingManagerDetailView.as_view(),name='manager_peer_testing_view'),
]