from django.views.generic.edit import CreateView 
from configurations.models import Series
import datetime 
from configurations.forms.SeriesForm import SeriesForm
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import user_passes_test
from configurations.HelperClasses.PermissionResolver import is_manager

class SeriesCreateView(LoginRequiredMixin,CreateView):
	model= Series
	form_class=SeriesForm
	template_name='configurations/create_view.html'
	redirect_field_name = None
	login_url ='/reviews/login'

	def form_valid(self, form):
		form.instance.last_update_by=self.request.user
		form.instance.created_by=self.request.user
		form.instance.creation_date=datetime.datetime.now()
		messages.success(self.request, 'Successfully created series : '+form.instance.series_name)
		return super().form_valid(form)

	def get_context_data(self, **kwargs):
		context=super(SeriesCreateView,self).get_context_data(**kwargs)
		context['page_title']='Create Series'
		context['card_title']='Series'
		context['is_conf_active']='active'
		return context

	@method_decorator(user_passes_test(is_manager,login_url='/reviews/unauthorized'))
	def dispatch(self, *args, **kwargs):
		return super(SeriesCreateView, self).dispatch(*args, **kwargs)

