from django.urls import path

from . import views
from django.conf.urls import url

from peer_testing.ListViews import(
	PeerTestingReviewListView,
	PeerTestingReviewRaisedToMeListView,
)
from peer_testing.UpdateViews import(
	PeerTestingApproveView
)
from peer_testing.DetailViews import(
	PeerTestingDetailView,
	PeerTestingApprovalDetailView
)
app_name='peer_testing'

urlpatterns = [
	path('peer_testing_home',views.peer_testing_home,name='peer_testing_home'),
	path('peer_testing_list',PeerTestingReviewListView.as_view(),name='peer_testing_list_view'),
	path('peer_testing_raised_to_me',PeerTestingReviewRaisedToMeListView.as_view(),name='peer_testing_raised_to_me'),
	url(r'^peer_testing_view/(?P<obj_pk>\d+)$',PeerTestingDetailView.as_view(),name='peer_testing_detail_view'),
	path('peer_testing_create',views.raise_peer_testing,name='peer_testing_create_view'),
	url(r'^peer_testing_approve/(?P<obj_pk>\d+)$',PeerTestingApproveView.as_view(),name='peer_testing_approve'),
	url(r'^peer_testing_approve_detail_view/(?P<obj_pk>\d+)$',PeerTestingApprovalDetailView.as_view(),name='peer_testing_approve_detail_view'),
	url(r'^peer_testing_update/(?P<obj_pk>\d+)$',views.update_peer_testing_review,name='peer_testing_update')
]