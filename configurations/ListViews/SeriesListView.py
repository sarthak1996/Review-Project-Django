from django.views.generic import ListView
from configurations.models import Series
from configurations.FilterSets import SeriesFilter
from collections import OrderedDict
from peer_review.HelperClasses import CommonLookups
from configurations.HelperClasses import SearchFilterBadges,SearchDropDown
class SeriesListView(ListView):
	model=Series
	template_name='configurations/list_view.html'


	def get_context_data(self,**kwargs):
		context = super().get_context_data(**kwargs)
		context['create_url']='configurations:series_create_view'
		context['create_object_button_title']='Create Series'
		context['detail_view_url']='configurations:series_detail_view'
		context['page_title']='Series'
		context['create_button_rendered']=True

		get_request=self.request.GET
		f_series_name=get_request.get('filter_form-series_name__icontains',None)
		f_series_type=get_request.get('filter_form-series_type',None)
		print('Generating filter tags')
		print(f_series_type,f_series_name)

		filter_badge_dict=OrderedDict({'series_name: %':f_series_name,
							'series_type: ':f_series_type
							})
		print(filter_badge_dict)
		filter_badges_list=SearchFilterBadges.generate_filter_badges_list(**filter_badge_dict)
		context['filter_badges']=filter_badges_list
		context['text_filters_drop_down_icon']=''

		context['filter']=SeriesFilter(self.request.GET,queryset=self.get_queryset(),prefix='filter_form')
		
		context['initial_filter']='Series name'
		context['other_filters']=None

		search_drop_downs_kwargs=OrderedDict({'filter_form-series_type':CommonLookups.get_series_types()})
		search_drop_downs_args=['Series type']
		#mandatory search drop down
		search_drop_downs=SearchDropDown.generate_drop_down_list(*search_drop_downs_args,**search_drop_downs_kwargs)
		context['search_drop_downs']=search_drop_downs
		context['reset_filters']='configurations:series_list_view'
		# context['actions_drop']=Actions.get_actions_for_configuration_objects('configurations:series_update_view')

		return context