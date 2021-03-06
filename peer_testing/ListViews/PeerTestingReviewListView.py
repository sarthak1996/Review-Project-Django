from django.views.generic import ListView
from peer_review.models import Review
from peer_review.HelperClasses import StatusCodes,CommonLookups,CommonCounts
from collections import OrderedDict
from configurations.HelperClasses import SearchFilterBadges,SearchDropDown,PaginationHelper
from peer_testing.FilterSets import PeerTestingFilter
from collections import OrderedDict
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import user_passes_test,login_required
from configurations.HelperClasses.PermissionResolver import is_emp_or_manager
from configurations.models import Team
from configurations.HelperClasses import LoggingHelper
import traceback
class PeerTestingReviewListView(ListView):
	model=Review
	template_name='configurations/list_view.html'
	redirect_field_name = None
	login_url ='/reviews/login'


	def get_context_data(self,**kwargs):
		context = super().get_context_data(**kwargs)
		logger=LoggingHelper(self.request.user,__name__)
		context['create_url']='peer_testing:peer_testing_create_view'
		context['create_object_button_title']='Create Peer Testing'
		context['detail_view_url']='peer_testing:peer_testing_detail_view'
		context['page_title']='Peer Testing'
		context['create_button_rendered']=True
		context['is_peer_test_active']='active'
		context['list_view_type']='peer_testing_list_view'
		context['logged_in_user']=self.request.user

		get_request=self.request.GET
		f_bug_number=get_request.get('filter_form-bug_number__icontains',None)
		f_raised_to=get_request.get('filter_form-raised_to',None)
		f_priority=get_request.get('filter_form-priority',None)
		f_approval_outcome=get_request.get('filter_form-approval_outcome',None)
		f_team=get_request.get('filter_form-team',None)
		# f_review_type=get_request.get('filter_form-review_type',None)
		# f_series_type=get_request.get('filter_form-series_type',None)

		logger.write('Generating filter tags',LoggingHelper.DEBUG)
		logger.write(str(f_bug_number),LoggingHelper.DEBUG)
		logger.write(str(f_raised_to),LoggingHelper.DEBUG)
		logger.write(str(f_priority),LoggingHelper.DEBUG)
		logger.write(str(f_approval_outcome),LoggingHelper.DEBUG)
		logger.write(str(f_team),LoggingHelper.DEBUG)


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
							'team: ':Team.objects.get(pk=f_team).team_name if f_team else None
							})
		logger.write(str(filter_badge_dict),LoggingHelper.DEBUG)
		filter_badges_list=SearchFilterBadges.generate_filter_badges_list(self.request,**filter_badge_dict)
		context['filter_badges']=filter_badges_list
		context['text_filters_drop_down_icon']='dropdown-toggle'

		context['filter']=PeerTestingFilter(self.request.GET,queryset=self.get_queryset(),prefix='filter_form')
		context['page_obj']=PaginationHelper.get_page_obj(context['filter'],get_request)


		# context['initial_filter']=''
		context['other_filters']={'filter_form-bug_number__icontains':'Bug number contains',
									'filter_form-raised_to':'Raised to contains'}.items()

		search_drop_downs_kwargs=OrderedDict({'filter_form-priority':CommonLookups.get_review_priorities(),
									'filter_form-approval_outcome':CommonLookups.get_approval_outcomes(),
									'filter_form-team':CommonLookups.get_team_lov(Team.objects.all())
									})
		search_drop_downs_args=['Priority','Approval outcome','Team']
		#mandatory search drop down
		search_drop_downs=SearchDropDown.generate_drop_down_list(self.request,*search_drop_downs_args,**search_drop_downs_kwargs)
		context['search_drop_downs']=search_drop_downs
		
		context['reset_filters']='peer_testing:peer_testing_list_view'
		context['progressbar']=True
		progress_dict=CommonCounts.get_perct_num_reviews_by_apr_outcome(qs=CommonCounts.get_peer_testing_raised_by_me(self.request.user),
																		user=self.request.user,
																		review_type=CommonLookups.get_peer_testing_question_type(),
																		request=self.request,
																		raised_to_me=False)
		context={**context,**progress_dict}
		logger.write('Context:'+str(context),LoggingHelper.DEBUG)
		return context

	def get_queryset(self):
		req=self.request 
		return Review.objects.filter(created_by=req.user,review_type=CommonLookups.get_peer_testing_question_type()).all().order_by('-last_update_date')



	@method_decorator(login_required(login_url='/reviews/login'))
	@method_decorator(user_passes_test(is_emp_or_manager,login_url='/reviews/unauthorized'))
	def dispatch(self, *args, **kwargs):
		return super(PeerTestingReviewListView, self).dispatch(*args, **kwargs)

		