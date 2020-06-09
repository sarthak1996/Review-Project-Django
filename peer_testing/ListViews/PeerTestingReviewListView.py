from django.views.generic import ListView
from peer_review.models import Review
from peer_review.HelperClasses import StatusCodes,CommonLookups
from collections import OrderedDict
from configurations.HelperClasses import SearchFilterBadges,SearchDropDown,PaginationHelper
from peer_testing.FilterSets import PeerTestingFilter
from collections import OrderedDict
class PeerTestingReviewListView(ListView):
	model=Review
	template_name='configurations/list_view.html'


	def get_context_data(self,**kwargs):
		context = super().get_context_data(**kwargs)
		context['create_url']='peer_testing:peer_testing_create_view'
		context['create_object_button_title']='Create Peer Testing'
		context['detail_view_url']='peer_testing:peer_testing_detail_view'
		context['page_title']='Peer Testing'
		context['create_button_rendered']=True

		get_request=self.request.GET
		f_bug_number=get_request.get('filter_form-bug_number__icontains',None)
		f_raised_to=get_request.get('filter_form-raised_to',None)
		f_priority=get_request.get('filter_form-priority',None)
		f_approval_outcome=get_request.get('filter_form-approval_outcome',None)
		f_team=get_request.get('filter_form-team',None)
		# f_review_type=get_request.get('filter_form-review_type',None)
		# f_series_type=get_request.get('filter_form-series_type',None)

		print('Generating filter tags')
		print(f_bug_number,f_raised_to,f_priority,f_approval_outcome,f_team)


		applied_filter_dict={
				'filter_form-bug_number__icontains':f_bug_number,
				'filter_form-raised_to':f_raised_to,
				'filter_form-priority':f_priority,
				'filter_form-approval_outcome':f_approval_outcome,
				'filter_form-team':f_team
		}
		context['applied_filters_params']=PaginationHelper.get_applied_filters_url(applied_filter_dict)


		filter_badge_dict=OrderedDict({'bug_number: %':f_bug_number,
							'raised_to: %':f_raised_to,
							'priority: ':f_priority,
							'approval_outcome: ':f_approval_outcome,
							'team: ':f_team
							})
		print(filter_badge_dict)
		filter_badges_list=SearchFilterBadges.generate_filter_badges_list(**filter_badge_dict)
		context['filter_badges']=filter_badges_list
		context['text_filters_drop_down_icon']='dropdown-toggle'

		context['filter']=PeerTestingFilter(self.request.GET,queryset=self.get_queryset(),prefix='filter_form')
		context['page_obj']=PaginationHelper.get_page_obj(context['filter'],get_request)


		# context['initial_filter']=''
		context['other_filters']={'filter_form-bug_number__icontains':'Bug number contains',
									'filter_form-raised_to':'Raised to contains'}.items()

		search_drop_downs_kwargs=OrderedDict({'filter_form-priority':CommonLookups.get_review_priorities(),
									'filter_form-approval_outcome':CommonLookups.get_approval_outcomes()
									})
		search_drop_downs_args=['Priority','Approval outcome']
		#mandatory search drop down
		search_drop_downs=SearchDropDown.generate_drop_down_list(*search_drop_downs_args,**search_drop_downs_kwargs)
		context['search_drop_downs']=search_drop_downs
		
		context['reset_filters']='peer_testing:peer_testing_list_view'
		return context

	def get_queryset(self):
		req=self.request 
		return Review.objects.filter(created_by=req.user,review_type=CommonLookups.get_peer_testing_question_type()).all()