from django.views.generic.detail import DetailView

from configurations.models import Series
from django.contrib.auth.mixins import LoginRequiredMixin

class SeriesDetailView(LoginRequiredMixin,DetailView):
	model=Series
	template_name='configurations/detail_view.html'
	context_object_name ='detail_obj'
	pk_url_kwarg='obj_pk'
	redirect_field_name = None
	login_url ='/reviews/login'

	def get_context_data(self, **kwargs):
		context=super(SeriesDetailView,self).get_context_data(**kwargs)
		series_obj=self.object
		context['detail_view_card_title']='Series'
		context['detail_name']=series_obj.series_name
		context['name_first_letter']=context['detail_name'][0]
		context['detail_view_title']='Series'
		context['update_view_url']='configurations:series_update_view'
		context['button_label']='Update'
		context['update_rendered']=True
		context['delegate_rendered']=False
		context['delegate_label']='Delegate'
		context['delegate_view_url']='peer_review:delegate_view'
		context['is_conf_active']='active'
		return context