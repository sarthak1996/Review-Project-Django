from django.views.generic import ListView
from configurations.models import Question

class QuestionListView(ListView):
	model=Question
	template_name='configurations/list_view.html'


	def get_context_data(self,**kwargs):
		context = super().get_context_data(**kwargs)
		context['create_url']='configurations:question_create_view'
		context['create_object_button_title']='Create Question'
		context['detail_view_url']='configurations:question_detail_view'
		context['page_title']='Question'
		context['create_button_rendered']=True
		return context