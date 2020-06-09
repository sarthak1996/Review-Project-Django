from django.views.generic.edit import UpdateView 
from configurations.models import Question
from configurations.forms.QuestionForm import QuestionForm
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin

class QuestionUpdateView(LoginRequiredMixin,UpdateView):
	model=Question
	template_name='configurations/create_view.html'
	# fields=['question_text','question_choice_type','mandatory','series_type','question_type','choices']
	form_class=QuestionForm
	pk_url_kwarg='obj_pk'
	redirect_field_name = None
	login_url ='/reviews/login'

	def form_valid(self, form):
		form.instance.last_update_by=self.request.user
		messages.success(self.request, 'Successfully updated question : '+form.instance.question_text)
		return super().form_valid(form)

	def get_context_data(self, **kwargs):
		context=super(QuestionUpdateView,self).get_context_data(**kwargs)
		context['page_title']='Update Question'
		context['card_title']='Question'
		context['dependent_choice']=True
		context['choice_dependent_url']='configurations:ajax_choices_for_questions'
		context['is_conf_active']='active'
		return context