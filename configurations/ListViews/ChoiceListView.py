from django.views.generic import ListView
from configurations.models import Choice

class ChoiceListView(ListView):
	model=Choice
	template_name='configurations/list_view.html'


	def get_context_data(self,**kwargs):
		context = super().get_context_data(**kwargs)
		context['create_url']='configurations:choice_create_view'
		context['create_object_button_title']='Create Choice'
		context['detail_view_url']='configurations:choice_detail_view'
		context['page_title']='Choice'
		context['create_button_rendered']=True
		return context