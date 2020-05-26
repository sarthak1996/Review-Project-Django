from django.views.generic import ListView
from configurations.models import Series

class SeriesListView(ListView):
	model=Series
	template_name='configurations/list_view.html'


	def get_context_data(self,**kwargs):
		context = super().get_context_data(**kwargs)
		context['create_url']='configurations:series_create_view'
		context['create_object_button_title']='Create Series'
		context['detail_view_url']='configurations:series_detail_view'
		context['page_title']='Series'
		context['create_button_rendered']=True
		return context