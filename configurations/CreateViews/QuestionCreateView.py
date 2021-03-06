from django.views.generic.edit import CreateView 
from configurations.models import Question
import datetime 
from configurations.forms.QuestionForm import QuestionForm
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import user_passes_test,login_required
from configurations.HelperClasses.PermissionResolver import is_manager
from configurations.HelperClasses import LoggingHelper
import traceback
class QuestionCreateView(CreateView):
	model= Question
	form_class=QuestionForm
	template_name='configurations/create_view.html'
	redirect_field_name = None
	login_url ='/reviews/login'
	
	def form_valid(self, form):
		try:
			redirect=super().form_valid(form)
		except Exception as e:
			form.add_error(None,str(e))
			logger=LoggingHelper(self.request.user,__name__)
			logger.write('Exception occurred: '+ str(traceback.format_exc()),LoggingHelper.ERROR)
			
			handle_exception()
			return super(QuestionCreateView,self).form_invalid(form)
		messages.success(self.request, 'Successfully created question : '+form.instance.question_text)
		return redirect

	def get_context_data(self, **kwargs):
		context=super(QuestionCreateView,self).get_context_data(**kwargs)
		context['page_title']='Create Question'
		context['card_title']='Question'
		context['dependent_choice']=True
		context['is_conf_active']='active'
		context['choice_dependent_url']='configurations:ajax_choices_for_questions'
		return context
		
	@method_decorator(login_required(login_url='/reviews/login'))
	@method_decorator(user_passes_test(is_manager,login_url='/reviews/unauthorized'))
	def dispatch(self, *args, **kwargs):
		return super(QuestionCreateView, self).dispatch(*args, **kwargs)