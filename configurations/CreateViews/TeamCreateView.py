from django.views.generic.edit import CreateView 
from configurations.models import Team
import datetime 
from configurations.forms.TeamForm import TeamForm
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import user_passes_test,login_required
from configurations.HelperClasses.PermissionResolver import is_manager

class TeamCreateView(CreateView):
	model= Team
	form_class=TeamForm
	template_name='configurations/create_view.html'
	redirect_field_name = None
	login_url ='/reviews/login'
	
	def form_valid(self, form):
		form.instance.last_update_by=self.request.user
		form.instance.created_by=self.request.user
		form.instance.creation_date=datetime.datetime.now()
		try:
			redirect=super().form_valid(form)
		except Exception as e:
			form.add_error(None,str(e))
			return super(TeamCreateView,self).form_invalid(form)
		messages.success(self.request, 'Successfully created team : '+form.instance.team_name)
		return redirect

	def get_context_data(self, **kwargs):
		context=super(TeamCreateView,self).get_context_data(**kwargs)
		context['page_title']='Create Team'
		context['card_title']='Team'
		context['is_conf_active']='active'
		return context

	@method_decorator(login_required(login_url='/reviews/login'))
	@method_decorator(user_passes_test(is_manager,login_url='/reviews/unauthorized'))
	def dispatch(self, *args, **kwargs):
		return super(TeamCreateView, self).dispatch(*args, **kwargs)
