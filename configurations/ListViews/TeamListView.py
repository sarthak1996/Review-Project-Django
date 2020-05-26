from django.views.generic import ListView
from configurations.models import Team

class TeamListView(ListView):
	model=Team
	template_name='configurations/list_view.html'


	def get_context_data(self,**kwargs):
		context = super().get_context_data(**kwargs)
		context['create_url']='configurations:team_create_view'
		context['create_object_button_title']='Create Team'
		context['detail_view_url']='configurations:team_detail_view'
		context['page_title']='Teams'
		context['create_button_rendered']=True
		return context
