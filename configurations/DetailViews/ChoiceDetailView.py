from django.views.generic.detail import DetailView

from configurations.models import Choice

class ChoiceDetailView(DetailView):
	model=Choice
	template_name='configurations/detail_view.html'
	context_object_name ='detail_obj'
	pk_url_kwarg='obj_pk'

	def get_context_data(self, **kwargs):
		context=super(ChoiceDetailView,self).get_context_data(**kwargs)
		choice_obj=self.object
		context['detail_view_card_title']='Choice'
		context['detail_name']=choice_obj.choice_text
		context['name_first_letter']=context['detail_name'][0]
		context['detail_view_title']='Choice'
		context['update_view_url']='configurations:choice_update_view'
		context['button_label']='Update'
		context['update_rendered']=True
		return context