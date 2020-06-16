from django.views.generic import ListView
from peer_review.models import Review
from peer_review.HelperClasses import StatusCodes,CommonLookups,CommonCounts
from configurations.HelperClasses import SearchFilterBadges,SearchDropDown,PaginationHelper
from peer_review.FilterSets import ReviewFilter
from collections import OrderedDict
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import user_passes_test,login_required
from configurations.HelperClasses.PermissionResolver import is_manager

class PeerReviewManagerListView(ListView):
	model=Review
	template_name='configurations/list_view.html'
	redirect_field_name = None
	login_url ='/reviews/login'


	def get_context_data(self,**kwargs):
		context = super().get_context_data(**kwargs)
		context['detail_view_url']='manager_activities:manager_review_view'
		context['page_title']='Peer Review - Manager'
		context['create_button_rendered']=False
		context['is_man_home_active']='active'
		context['list_view_type']='manager_view'
		context['logged_in_user']=self.request.user
		# context['restrict_by_user_prop']=True
		
		get_request=self.request.GET
		f_bug_number=get_request.get('filter_form-bug_number__icontains',None)
		f_raised_to=get_request.get('filter_form-raised_to',None)
		f_priority=get_request.get('filter_form-priority',None)
		f_approval_outcome=get_request.get('filter_form-approval_outcome',None)
		f_team=get_request.get('filter_form-team',None)
		# f_review_type=get_request.get('filter_form-review_type',None)
		f_series_type=get_request.get('filter_form-series_type',None)
		print('Generating filter tags')
		print(f_bug_number,f_raised_to,f_priority,f_approval_outcome,f_team,f_series_type)
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
							'team: ':f_team,
							'series_type: ':f_series_type
							})
		print(filter_badge_dict)
		filter_badges_list=SearchFilterBadges.generate_filter_badges_list(**filter_badge_dict)
		context['filter_badges']=filter_badges_list
		context['text_filters_drop_down_icon']='dropdown-toggle'

		context['filter']=ReviewFilter(self.request.GET,queryset=self.get_queryset(),prefix='filter_form')
		
		context['page_obj']=PaginationHelper.get_page_obj(context['filter'],get_request)

		# context['initial_filter']=''
		context['other_filters']={'filter_form-bug_number__icontains':'Bug number contains',
									'filter_form-raised_to':'Raised to contains'}.items()

		search_drop_downs_kwargs=OrderedDict({'filter_form-priority':CommonLookups.get_review_priorities(),
									'filter_form-approval_outcome':CommonLookups.get_approval_outcomes(),
									'filter_form-series_type':CommonLookups.get_series_types()
									})
		search_drop_downs_args=['Priority','Approval outcome','Series type']
		#mandatory search drop down
		search_drop_downs=SearchDropDown.generate_drop_down_list(*search_drop_downs_args,**search_drop_downs_kwargs)
		context['search_drop_downs']=search_drop_downs
		
		context['reset_filters']='manager_activities:peer_review_manager_list'
		# context['actions_drop']=Actions.get_actions_for_configuration_objects('configurations:team_update_view')

							
		context['progressbar']=True
		progress_dict=CommonCounts.get_perct_num_reviews_by_apr_outcome(qs=self.get_queryset(),
																		user=self.request.user,
																		review_type=CommonLookups.get_peer_review_question_type(),
																		raised_to_me=False,
																		from_manager=True)
		context={**context,**progress_dict}
		# print('Progress bar:')
		# print(context)

		return context

	def get_queryset(self):
		req=self.request 
		teams=[team for team in req.user.managed_teams.all()]
		return CommonCounts.get_review_raised_by_my_team(req.user,teams)
		


	@method_decorator(login_required(login_url='/reviews/login'))
	@method_decorator(user_passes_test(is_manager,login_url='/reviews/unauthorized'))
	def dispatch(self, *args, **kwargs):
		return super(PeerReviewManagerListView, self).dispatch(*args, **kwargs)