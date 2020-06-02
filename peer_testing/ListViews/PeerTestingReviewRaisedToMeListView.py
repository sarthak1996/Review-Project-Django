from django.views.generic import ListView
from peer_review.models import Review,Approval
from peer_review.HelperClasses import StatusCodes,CommonLookups
from configurations.HelperClasses import SearchFilterBadges,SearchDropDown
from peer_testing.FilterSets import PeerTestingRaisedToMeFilter
from collections import OrderedDict

class PeerTestingReviewRaisedToMeListView(ListView):
	model=Review
	template_name='configurations/list_view.html'
	# queryset=Approval.objects.filter(latest='True',raised_to=self.request.user).approval_review_assoc.all()
	def get_form_kwargs(self):
		kw = super(PeerTestingReviewRaisedToMeListView, self).get_form_kwargs()
		kw['request'] = self.request 
		return kw

	def get_context_data(self,**kwargs):
		context = super(PeerTestingReviewRaisedToMeListView,self).get_context_data(**kwargs)
		context['create_url']='peer_testing:peer_testing_create_view'
		context['create_object_button_title']='Create Peer Testing'
		context['detail_view_url']='peer_testing:peer_testing_approve_detail_view'
		context['page_title']='Peer Testing'
		context['create_button_rendered']=False
		# print()
		# print(Approval.objects.filter(latest='True',raised_to=self.request.user).approval_review_assoc.all())
		

		get_request=self.request.GET
		f_bug_number=get_request.get('filter_form-bug_number__icontains',None)
		f_priority=get_request.get('filter_form-priority',None)
		f_raised_by=get_request.get('filter_form-raised_by',None)
		# f_series_type=get_request.get('filter_form-series_type',None)
		
		print('Generating filter tags')
		print(f_bug_number,f_raised_by,f_priority)

		filter_badge_dict=OrderedDict({'bug_number: %':f_bug_number,
							'raised_by: %':f_raised_by,
							'priority: ':f_priority
							})
		print(filter_badge_dict)
		filter_badges_list=SearchFilterBadges.generate_filter_badges_list(**filter_badge_dict)
		context['filter_badges']=filter_badges_list
		context['text_filters_drop_down_icon']='dropdown-toggle'

		context['filter']=PeerTestingRaisedToMeFilter(self.request.GET,queryset=self.get_queryset(),prefix='filter_form')
		
		context['other_filters']={'filter_form-bug_number__icontains':'Bug number contains',
									'filter_form-raised_by':'Raised by contains'}.items()
		

		search_drop_downs_kwargs=OrderedDict({'filter_form-priority':CommonLookups.get_review_priorities()})
		search_drop_downs_args=['Priority']
		#mandatory search drop down
		search_drop_downs=SearchDropDown.generate_drop_down_list(*search_drop_downs_args,**search_drop_downs_kwargs)
		context['search_drop_downs']=search_drop_downs
		
		context['reset_filters']='peer_testing:peer_testing_raised_to_me'
		

		return context

	def get_queryset(self):
		return Review.objects.filter(approval_review_assoc__latest='True',approval_review_assoc__raised_to=self.request.user,approval_review_assoc__approval_outcome=StatusCodes.get_pending_status(),review_type=CommonLookups.get_peer_testing_question_type()).all()