from django.views.generic.edit import CreateView 
from configurations.models import Choice
import datetime 
from configurations.forms.ChoiceForm import ChoiceForm
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import user_passes_test,login_required
from configurations.HelperClasses.PermissionResolver import is_manager

class ChoiceCreateView(CreateView):
	model= Choice
	form_class=ChoiceForm
	template_name='configurations/create_view.html'
	redirect_field_name = None
	login_url ='/reviews/login'
	def form_valid(self, form):
		form.instance.last_update_by=self.request.user
		form.instance.created_by=self.request.user
		form.instance.creation_date=datetime.datetime.now()
		messages.success(self.request, 'Successfully created choice : '+form.instance.choice_text)
		return super().form_valid(form)

	def get_context_data(self, **kwargs):
		context=super(ChoiceCreateView,self).get_context_data(**kwargs)
		context['page_title']='Create Choice'
		context['card_title']='Choice'
		context['is_conf_active']='active'
		return context

	@method_decorator(login_required(login_url='/reviews/login'))
	@method_decorator(user_passes_test(is_manager,login_url='/reviews/unauthorized'))
	def dispatch(self, *args, **kwargs):
		return super(ChoiceCreateView, self).dispatch(*args, **kwargs)

