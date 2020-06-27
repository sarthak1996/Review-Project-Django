from django.views.generic.edit import CreateView 
from configurations.models import Series
import datetime 
from configurations.forms.SeriesForm import SeriesForm
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import user_passes_test,login_required
from configurations.HelperClasses.PermissionResolver import is_manager
from configurations.HelperClasses import LoggingHelper
import traceback
class SeriesCreateView(CreateView):
	model= Series
	form_class=SeriesForm
	template_name='configurations/create_view.html'
	redirect_field_name = None
	login_url ='/reviews/login'

	def form_valid(self, form):
		try:
			redirect=super().form_valid(form)
		except Exception as e:
			form.add_error(None,str(e))
			logger=LoggingHelper(self.request.user,__name__)
			logger.write('Exception occurred: '+ str(traceback.format_exc()),LoggingHelper.ERROR)
			
			handle_exception()
			return super(SeriesCreateView,self).form_invalid(form)
		messages.success(self.request, 'Successfully created series : '+form.instance.series_name)
		return redirect

	def get_context_data(self, **kwargs):
		context=super(SeriesCreateView,self).get_context_data(**kwargs)
		context['page_title']='Create Series'
		context['card_title']='Series'
		context['is_conf_active']='active'
		return context
	
	@method_decorator(login_required(login_url='/reviews/login'))
	@method_decorator(user_passes_test(is_manager,login_url='/reviews/unauthorized'))
	def dispatch(self, *args, **kwargs):
		return super(SeriesCreateView, self).dispatch(*args, **kwargs)

