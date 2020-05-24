from django.views.generic.edit import UpdateView 
from configurations.models import Team
from configurations.forms.TeamForm import TeamForm

class TeamUpdateView(UpdateView):
	model=Team
	template_name='configurations/create_view.html'
	# fields=[
	# 	'team_name',
	# 	'team_grp_mail',
	# ]
	form_class=TeamForm
	pk_url_kwarg='obj_pk'

	def form_valid(self, form):
		form.instance.last_update_by=self.request.user
		return super().form_valid(form)

	def get_context_data(self, **kwargs):
		context=super(TeamUpdateView,self).get_context_data(**kwargs)
		context['page_title']='Update Team'
		context['card_title']='Team'
		return context