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

from manager_activities.UpdateViews import(
	FollowUpManagerUpdateView
)

app_name='manager_activities'

urlpatterns =[
	path('manager_home',views.manager_view_landing_page,name='manager_home'),
	path('peer_review_manager_list',PeerReviewManagerListView.as_view(),name='peer_review_manager_list'),
	path('peer_testing_manager_list',PeerTestingManagerListView.as_view(),name='peer_testing_manager_list'),
	url(r'^manager_review_view/(?P<obj_pk>\d+)$',PeerReviewManagerDetailView.as_view(),name='manager_review_view'),
	url(r'^manager_peer_testing_view/(?P<obj_pk>\d+)$',PeerTestingManagerDetailView.as_view(),name='manager_peer_testing_view'),
	path('ajax_peer_testing_graph_manager',views.peer_testing_graph_manager,name='ajax_peer_testing_graph_manager'),
	path('ajax_peer_review_graph_manager',views.peer_review_graph_manager,name='ajax_peer_review_graph_manager'),
	url(r'^follow_up_manager/(?P<obj_pk>\d+)$',FollowUpManagerUpdateView.as_view(),name='follow_up_manager')
]