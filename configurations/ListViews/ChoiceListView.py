from django.views.generic import ListView
from configurations.models import Choice
from configurations.HelperClasses import SearchFilterBadges,PaginationHelper
from configurations.FilterSets import ChoiceFilter
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import user_passes_test,login_required
from configurations.HelperClasses.PermissionResolver import is_manager
from configurations.HelperClasses import LoggingHelper
import traceback
class ChoiceListView(ListView):
	model=Choice
	template_name='configurations/list_view.html'
	redirect_field_name = None
	login_url ='/reviews/login'

	def get_context_data(self,**kwargs):
		context = super().get_context_data(**kwargs)
		logger=LoggingHelper(self.request.user,__name__)
		context['create_url']='configurations:choice_create_view'
		context['create_object_button_title']='Create Choice'
		context['detail_view_url']='configurations:choice_detail_view'
		context['page_title']='Choice'
		context['create_button_rendered']=True
		context['is_conf_active']='active'
		

		get_request=self.request.GET
		f_choice_text=get_request.get('filter_form-choice_text__icontains',None)	
		logger.write('Generating filter tags',LoggingHelper.DEBUG)
		logger.write('filter:'+str(f_choice_text),LoggingHelper.DEBUG)
		
		
		applied_filter_dict={
			'filter_form-choice_text__icontains':f_choice_text
		}
		context['applied_filters_params']=PaginationHelper.get_applied_filters_url(applied_filter_dict)

		filter_badge_dict={'choice_text: %':f_choice_text}
		filter_badges_list=SearchFilterBadges.generate_filter_badges_list(self.request,**filter_badge_dict)
		context['filter_badges']=filter_badges_list
		context['text_filters_drop_down_icon']=''

		context['filter']=ChoiceFilter(self.request.GET,queryset=self.get_queryset(),prefix='filter_form')
		
		context['page_obj']=PaginationHelper.get_page_obj(context['filter'],get_request)

		context['initial_filter']='Choice text'
		context['other_filters']=None
		context['search_drop_downs']=None
		context['logged_in_user']=self.request.user
		context['reset_filters']='configurations:choice_list_view'
		# context['actions_drop']=Actions.get_actions_for_configuration_objects('configurations:choice_update_view')
		logger.write('context:'+str(context),LoggingHelper.DEBUG)
		return context


	@method_decorator(login_required(login_url='/reviews/login'))
	@method_decorator(user_passes_test(is_manager,login_url='/reviews/unauthorized'))
	def dispatch(self, *args, **kwargs):
		return super(ChoiceListView, self).dispatch(*args, **kwargs)

	def get_queryset(self):
		return Choice.objects.all().order_by('choice_text')
