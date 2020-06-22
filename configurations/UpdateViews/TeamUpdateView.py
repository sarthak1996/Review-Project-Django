from django.views.generic.edit import UpdateView 
from configurations.models import Team
from configurations.forms.TeamForm import TeamForm
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import user_passes_test,login_required
from configurations.HelperClasses.PermissionResolver import is_manager
from django.urls import reverse_lazy
from django.db import transaction
from datetime import datetime
from django.utils import timezone


class TeamUpdateView(UpdateView):
	model=Team
	template_name='configurations/create_view.html'
	# fields=[
	# 	'team_name',
	# 	'team_grp_mail',
	# ]
	form_class=TeamForm
	pk_url_kwarg='obj_pk'
	redirect_field_name = None
	login_url ='/reviews/login'

	@transaction.atomic
	def form_valid(self, form):
		form.instance.last_update_by=self.request.user
		try :
			redirect = super().form_valid(form)
		except Exception as e:
			form.add_error(None,str(e))
			handle_exception()
			return super(TeamUpdateView,self).form_invalid(form)
		messages.success(self.request, 'Successfully updated team : '+form.instance.team_name)
		return redirect

	def get_context_data(self, **kwargs):
		context=super(TeamUpdateView,self).get_context_data(**kwargs)
		context['page_title']='Update Team'
		context['card_title']='Team'
		context['is_conf_active']='active'
		return context


	@method_decorator(login_required(login_url='/reviews/login'))
	@method_decorator(user_passes_test(is_manager,login_url='/reviews/unauthorized'))
	def dispatch(self, *args, **kwargs):
		return super(TeamUpdateView, self).dispatch(*args, **kwargs)



		