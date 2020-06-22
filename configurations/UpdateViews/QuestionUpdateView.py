from django.views.generic.edit import UpdateView 
from configurations.models import Question
from configurations.forms.QuestionForm import QuestionForm
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import user_passes_test,login_required
from configurations.HelperClasses.PermissionResolver import is_manager
from django.urls import reverse_lazy
from django.db import transaction

class QuestionUpdateView(UpdateView):
	model=Question
	template_name='configurations/create_view.html'
	# fields=['question_text','question_choice_type','mandatory','series_type','question_type','choices']
	form_class=QuestionForm
	pk_url_kwarg='obj_pk'
	redirect_field_name = None
	login_url ='/reviews/login'

	@transaction.atomic
	def form_valid(self, form):
		form.instance.last_update_by=self.request.user
		try :
			redirect = super().form_valid(form)
		except Exception as e:
			form.add_error(None,str(e))
			handle_exception()
			return super(QuestionUpdateView,self).form_invalid(form)
		messages.success(self.request, 'Successfully updated question : '+form.instance.question_text)
		return redirect

	def get_context_data(self, **kwargs):
		context=super(QuestionUpdateView,self).get_context_data(**kwargs)
		context['page_title']='Update Question'
		context['card_title']='Question'
		context['dependent_choice']=True
		context['choice_dependent_url']='configurations:ajax_choices_for_questions'
		context['is_conf_active']='active'
		return context


	@method_decorator(login_required(login_url='/reviews/login'))
	@method_decorator(user_passes_test(is_manager,login_url='/reviews/unauthorized'))
	def dispatch(self, *args, **kwargs):
		return super(QuestionUpdateView, self).dispatch(*args, **kwargs)


		