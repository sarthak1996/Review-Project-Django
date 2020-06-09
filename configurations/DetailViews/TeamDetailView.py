from django.views.generic.detail import DetailView

from configurations.models import Team

class TeamDetailView(DetailView):
	model=Team
	template_name='configurations/detail_view.html'
	context_object_name ='detail_obj'
	pk_url_kwarg='obj_pk'

	def get_context_data(self, **kwargs):
		context=super(TeamDetailView,self).get_context_data(**kwargs)
		team_obj=self.object
		context['detail_view_card_title']='Team'
		context['detail_name']=team_obj.team_name
		context['name_first_letter']=context['detail_name'][0]
		context['detail_view_title']='Team'
		context['update_view_url']='configurations:team_update_view'
		context['button_label']='Update'
		context['update_rendered']=True
		context['delegate_rendered']=False
		context['delegate_label']='Delegate'
		context['delegate_view_url']='peer_review:delegate_view'
		context['is_conf_active']='active'
		return context