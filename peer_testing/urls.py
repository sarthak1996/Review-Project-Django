from django.urls import path

from . import views
from django.conf.urls import url

from peer_testing.ListViews import(
	PeerTestingReviewListView,
	PeerTestingReviewRaisedToMeListView,
)
from peer_testing.UpdateViews import(
	PeerTestingApproveView,
	RejectPeerTestingUpdateView,
	FollowUpPeerTestingUpdateView
)
from peer_testing.DetailViews import(
	PeerTestingDetailView,
	PeerTestingApprovalDetailView
)
from peer_testing.CreateViews import(
	DelegatePeerTestApprovalCreateView
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
	url(r'^peer_testing_update/(?P<obj_pk>\d+)$',views.update_peer_testing_review,name='peer_testing_update'),
	url(r'^delegate_approval_peer_test/(?P<obj_pk>\d+)$',DelegatePeerTestApprovalCreateView.as_view(),name='delegate_peer_test'),
	url(r'^reject_peer_test/(?P<obj_pk>\d+)$',RejectPeerTestingUpdateView.as_view(),name='reject_peer_test'),
	url(r'^follow_up_peer_test/(?P<obj_pk>\d+)$',FollowUpPeerTestingUpdateView.as_view(),name='follow_up_peer_test'),
	url(r'^invalidate_peer_test/(?P<obj_pk>\d+)$',views.invalidate_peer_test,name='invalidate_peer_test'),
   	
   	
]