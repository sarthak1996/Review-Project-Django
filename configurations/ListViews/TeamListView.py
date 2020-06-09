from django.views.generic import ListView
from configurations.models import Team
from collections import OrderedDict
from configurations.HelperClasses import SearchFilterBadges,SearchDropDown,PaginationHelper
from configurations.FilterSets import TeamFilter
class TeamListView(ListView):
	model=Team
	template_name='configurations/list_view.html'


	def get_context_data(self,**kwargs):
		context = super().get_context_data(**kwargs)
		context['create_url']='configurations:team_create_view'
		context['create_object_button_title']='Create Team'
		context['detail_view_url']='configurations:team_detail_view'
		context['page_title']='Teams'
		context['create_button_rendered']=True

		get_request=self.request.GET
		f_team_name=get_request.get('filter_form-team_name__icontains',None)
		f_team_grp_mail=get_request.get('filter_form-team_grp_mail__icontains',None)
		print('Generating filter tags')
		print(f_team_name,f_team_grp_mail)
		
		applied_filter_dict={
				'filter_form-team_name__icontains':f_team_name,
				'filter_form-team_grp_mail__icontains':f_team_grp_mail
		}
		context['applied_filters_params']=PaginationHelper.get_applied_filters_url(applied_filter_dict)



		filter_badge_dict=OrderedDict({'team_name: %':f_team_name,
							'team_grp_mail: %':f_team_grp_mail
							})
		print(filter_badge_dict)
		filter_badges_list=SearchFilterBadges.generate_filter_badges_list(**filter_badge_dict)
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


		return context
