from django.views.generic.detail import DetailView

from configurations.models import Question

class QuestionDetailView(DetailView):
	model=Question
	template_name='configurations/detail_view.html'
	context_object_name ='detail_obj'
	pk_url_kwarg='obj_pk'

	def get_context_data(self, **kwargs):
		context=super(QuestionDetailView,self).get_context_data(**kwargs)
		question_obj=self.object
		context['detail_view_card_title']='Question'
		context['detail_name']=question_obj.question_text
		context['name_first_letter']=context['detail_name'][0]
		context['detail_view_title']='Question'
		context['update_view_url']='configurations:question_update_view'
		context['button_label']='Update'
		return context