from django.urls import path

from . import views
from django.conf.urls import url
from peer_review.ListViews import(
	ReviewListView,
	ReviewRaisedToMeListView
	)
from peer_review.DetailViews import(
	ReviewDetailView,
	ReviewRaisedToMeDetailView
	)
from peer_review.UpdateViews import(
	ReviewUpdateView
	)
from peer_review.CreateViews import(
	ReviewCreateView,
	DelegateReviewApprovalCreateView
	)

app_name='peer_review'

urlpatterns =[
	path('review',ReviewListView.as_view(),name='review_list_view'),
    url(r'^review_view/(?P<obj_pk>\d+)$',ReviewDetailView.as_view(),name='review_detail_view'),
    url(r'^review_update_view/(?P<obj_pk>\d+)$',ReviewUpdateView.as_view(),name='review_update_view'),
    path('review/create',ReviewCreateView.as_view(),name='review_create_view'),
    path('review_home',views.reviews_home,name='review_home'),
    path('review_raised_to_me',ReviewRaisedToMeListView.as_view(),name='review_raised_to_me'),
    url(r'^review_detail_approve_view/(?P<obj_pk>\d+)$',views.peer_review_approval_form,name='review_detail_approve_view'),
   	url(r'^delegate_approval/(?P<obj_pk>\d+)$',DelegateReviewApprovalCreateView.as_view(),name='delegate_review'),
   	url(r'^invalidate_review/(?P<obj_pk>\d+)$',views.invalidate_review,name='invalidate_review'),
   	url(r'^reject_review/(?P<obj_pk>\d+)$',views.reject_review,name='reject_review'),
   	path('ajax/load_raise_to_review',views.load_users_based_on_team,name='ajax_load_raise_to_lov')
]