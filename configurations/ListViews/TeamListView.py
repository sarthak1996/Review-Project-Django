from django.views.generic import ListView
from configurations.models import Team
from collections import OrderedDict
from configurations.HelperClasses import SearchFilterBadges,SearchDropDown,PaginationHelper
from configurations.FilterSets import TeamFilter
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import user_passes_test,login_required
from configurations.HelperClasses.PermissionResolver import is_manager
from configurations.HelperClasses import LoggingHelper
import traceback
class TeamListView(ListView):
	model=Team
	template_name='configurations/list_view.html'
	redirect_field_name = None
	login_url ='/reviews/login'


	def get_context_data(self,**kwargs):
		context = super().get_context_data(**kwargs)
		logger=LoggingHelper(self.request.user,__name__)
		context['create_url']='configurations:team_create_view'
		context['create_object_button_title']='Create Team'
		context['detail_view_url']='configurations:team_detail_view'
		context['page_title']='Teams'
		context['create_button_rendered']=True
		context['is_conf_active']='active'
		get_request=self.request.GET
		f_team_name=get_request.get('filter_form-team_name__icontains',None)
		f_team_grp_mail=get_request.get('filter_form-team_grp_mail__icontains',None)
		logger.write('Generating filter tags',LoggingHelper.DEBUG)
		logger.write(f_team_name,LoggingHelper.DEBUG)
		logger.write(f_team_grp_mail,LoggingHelper.DEBUG)
		
		applied_filter_dict={
				'filter_form-team_name__icontains':f_team_name,
				'filter_form-team_grp_mail__icontains':f_team_grp_mail
		}
		context['applied_filters_params']=PaginationHelper.get_applied_filters_url(applied_filter_dict)



		filter_badge_dict=OrderedDict({'team_name: %':f_team_name,
							'team_grp_mail: %':f_team_grp_mail
							})
		filter_badges_list=SearchFilterBadges.generate_filter_badges_list(self.request,**filter_badge_dict)
		context['filter_badges']=filter_badges_list
		context['text_filters_drop_down_icon']='dropdown-toggle'

		context['filter']=TeamFilter(self.request.GET,queryset=self.get_queryset(),prefix='filter_form')
		
		context['page_obj']=PaginationHelper.get_page_obj(context['filter'],get_request)

		context['initial_filter']='Team name'
		context['other_filters']={'filter_form-team_name__icontains':'Team name contains',
									'filter_form-team_grp_mail__icontains':'Team grp mail contains'}.items()

		context['search_drop_downs']=None
		context['reset_filters']='configurations:team_list_view'
		
		# context['actions_drop']=Actions.get_actions_for_configuration_objects('configurations:team_update_view')

		context['logged_in_user']=self.request.user
		logger.write('context:'+str(context),LoggingHelper.DEBUG)
		return context


	@method_decorator(login_required(login_url='/reviews/login'))
	@method_decorator(user_passes_test(is_manager,login_url='/reviews/unauthorized'))
	def dispatch(self, *args, **kwargs):
		return super(TeamListView, self).dispatch(*args, **kwargs)

	def get_queryset(self):
		return Team.objects.all().order_by('team_name')

		
