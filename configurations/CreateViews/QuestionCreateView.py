from django.views.generic.edit import CreateView 
from configurations.models import Question
import datetime 
from configurations.forms.QuestionForm import QuestionForm
from django.contrib import messages
class QuestionCreateView(CreateView):
	model= Question
	form_class=QuestionForm
	template_name='configurations/create_view.html'

	def form_valid(self, form):
		form.instance.last_update_by=self.request.user
		form.instance.created_by=self.request.user
		form.instance.creation_date=datetime.datetime.now()
		messages.success(self.request, 'Successfully created question : '+form.instance.question_text)
		return super().form_valid(form)

	def get_context_data(self, **kwargs):
		context=super(QuestionCreateView,self).get_context_data(**kwargs)
		context['page_title']='Create Question'
		context['card_title']='Question'
		context['dependent_choice']=True
		context['is_conf_active']='active'
		context['choice_dependent_url']='configurations:ajax_choices_for_questions'
		return context