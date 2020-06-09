from django.views.generic.edit import UpdateView 
from configurations.models import Series
from configurations.forms.SeriesForm import SeriesForm
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import user_passes_test
from configurations.HelperClasses.PermissionResolver import is_manager

class SeriesUpdateView(LoginRequiredMixin,UpdateView):
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

	def form_valid(self, form):
		form.instance.last_update_by=self.request.user
		messages.success(self.request, 'Successfully updated series : '+form.instance.series_name)
		return super().form_valid(form)

	def get_context_data(self, **kwargs):
		context=super(SeriesUpdateView,self).get_context_data(**kwargs)
		context['page_title']='Update Series'
		context['card_title']='Series'
		context['is_conf_active']='active'
		return context


	@method_decorator(user_passes_test(is_manager,login_url='/reviews/unauthorized'))
	def dispatch(self, *args, **kwargs):
		return super(SeriesUpdateView, self).dispatch(*args, **kwargs)


		