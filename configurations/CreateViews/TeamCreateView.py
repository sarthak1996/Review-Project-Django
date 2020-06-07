from django.views.generic.edit import CreateView 
from configurations.models import Team
import datetime 
from configurations.forms.TeamForm import TeamForm
from django.contrib import messages
class TeamCreateView(CreateView):
	model= Team
	form_class=TeamForm
	template_name='configurations/create_view.html'

	def form_valid(self, form):
		form.instance.last_update_by=self.request.user
		form.instance.created_by=self.request.user
		form.instance.creation_date=datetime.datetime.now()
		messages.success(self.request, 'Successfully created team : '+form.instance.team_name)
		return super().form_valid(form)

	def get_context_data(self, **kwargs):
		context=super(SeriesCreateView,self).get_context_data(**kwargs)
		context['page_title']='Create Team'
		context['card_title']='Team'
		return context