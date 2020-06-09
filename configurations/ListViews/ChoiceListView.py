from django.views.generic import ListView
from configurations.models import Choice
from configurations.HelperClasses import SearchFilterBadges,PaginationHelper
from configurations.FilterSets import ChoiceFilter
class ChoiceListView(ListView):
	model=Choice
	template_name='configurations/list_view.html'


	def get_context_data(self,**kwargs):
		context = super().get_context_data(**kwargs)
		context['create_url']='configurations:choice_create_view'
		context['create_object_button_title']='Create Choice'
		context['detail_view_url']='configurations:choice_detail_view'
		context['page_title']='Choice'
		context['create_button_rendered']=True
		

		get_request=self.request.GET
		f_choice_text=get_request.get('filter_form-choice_text__icontains',None)	
		print('Generating filter tags')
		print(f_choice_text)
		
		applied_filter_dict={
			'filter_form-choice_text__icontains':f_choice_text
		}
		context['applied_filters_params']=PaginationHelper.get_applied_filters_url(applied_filter_dict)

		filter_badge_dict={'choice_text: %':f_choice_text}
		filter_badges_list=SearchFilterBadges.generate_filter_badges_list(**filter_badge_dict)
		context['filter_badges']=filter_badges_list
		context['text_filters_drop_down_icon']=''

		context['filter']=ChoiceFilter(self.request.GET,queryset=self.get_queryset(),prefix='filter_form')
		
		context['page_obj']=PaginationHelper.get_page_obj(context['filter'],get_request)

		context['initial_filter']='Choice text'
		context['other_filters']=None
		context['search_drop_downs']=None

		context['reset_filters']='configurations:choice_list_view'
		# context['actions_drop']=Actions.get_actions_for_configuration_objects('configurations:choice_update_view')

		return context