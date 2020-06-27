from django.views.generic.detail import DetailView

from configurations.models import Series
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import user_passes_test,login_required
from configurations.HelperClasses.PermissionResolver import is_manager
from configurations.HelperClasses import LoggingHelper
import traceback
class SeriesDetailView(DetailView):
	model=Series
	template_name='configurations/detail_view.html'
	context_object_name ='detail_obj'
	pk_url_kwarg='obj_pk'
	redirect_field_name = None
	login_url ='/reviews/login'

	def get_context_data(self, **kwargs):
		context=super(SeriesDetailView,self).get_context_data(**kwargs)
		series_obj=self.object
		context['detail_view_card_title']='Series'
		context['detail_name']=series_obj.series_name
		context['name_first_letter']=context['detail_name'][0]
		context['detail_view_title']='Series'
		context['update_view_url']='configurations:series_update_view'
		context['button_label']='Update'
		context['update_rendered']=True
		context['delegate_rendered']=False
		context['delegate_label']='Delegate'
		context['delegate_view_url']='peer_review:delegate_view'
		context['is_conf_active']='active'
		logger=LoggingHelper(self.request.user,__name__)
		logger.write('Context:'+str(context),LoggingHelper.DEBUG)
		return context


	@method_decorator(login_required(login_url='/reviews/login'))
	@method_decorator(user_passes_test(is_manager,login_url='/reviews/unauthorized'))
	def dispatch(self, *args, **kwargs):
		return super(SeriesDetailView, self).dispatch(*args, **kwargs)