from django.views.generic.edit import UpdateView 
from configurations.models import Series
from configurations.forms.SeriesForm import SeriesForm
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import user_passes_test,login_required
from configurations.HelperClasses.PermissionResolver import is_manager
from django.urls import reverse_lazy
from django.db import transaction
from configurations.HelperClasses import LoggingHelper
import traceback
class SeriesUpdateView(UpdateView):
	model=Series
	template_name='configurations/create_view.html'
	# fields=[
	# 	'series_name',
	# 	'series_type',
	# ]
	form_class=SeriesForm
	pk_url_kwarg='obj_pk'
	redirect_field_name = None
	login_url ='/reviews/login'

	@transaction.atomic
	def form_valid(self, form):
		logger=LoggingHelper(self.request.user,__name__)
		try :
			redirect = super().form_valid(form)
		except Exception as e:
			form.add_error(None,str(e))
			logger.write('Exception:'+str(traceback.format_exc()),LoggingHelper.DEBUG)
			handle_exception()
			return super(SeriesUpdateView,self).form_invalid(form)
		messages.success(self.request, 'Successfully updated series : '+form.instance.series_name)
		return redirect

	def get_context_data(self, **kwargs):
		context=super(SeriesUpdateView,self).get_context_data(**kwargs)
		context['page_title']='Update Series'
		context['card_title']='Series'
		context['is_conf_active']='active'
		return context



	@method_decorator(login_required(login_url='/reviews/login'))
	@method_decorator(user_passes_test(is_manager,login_url='/reviews/unauthorized'))
	def dispatch(self, *args, **kwargs):
		return super(SeriesUpdateView, self).dispatch(*args, **kwargs)


		