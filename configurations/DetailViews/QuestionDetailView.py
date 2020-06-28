from django.views.generic.detail import DetailView

from configurations.models import Question
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import user_passes_test,login_required
from configurations.HelperClasses.PermissionResolver import is_manager
from configurations.HelperClasses import LoggingHelper
import traceback
class QuestionDetailView(DetailView):
	model=Question
	template_name='configurations/detail_view.html'
	context_object_name ='detail_obj'
	pk_url_kwarg='obj_pk'
	redirect_field_name = None
	login_url ='/reviews/login'

	def get_context_data(self, **kwargs):
		context=super(QuestionDetailView,self).get_context_data(**kwargs)
		question_obj=self.object
		context['detail_view_card_title']='Question'
		context['detail_name']=question_obj.question_text
		context['name_first_letter']=context['detail_name'][0]
		context['detail_view_title']='Question'
		context['update_view_url']='configurations:question_update_view'
		context['button_label']='Update'
		context['update_rendered']=True
		context['delegate_rendered']=False
		context['delegate_label']='Delegate'
		context['delegate_view_url']='peer_review:delegate_view'
		context['is_conf_active']='active'
		context['logged_in_user']=self.request.user
		logger=LoggingHelper(self.request.user,__name__)
		logger.write('Context:'+str(context),LoggingHelper.DEBUG)
		return context

	@method_decorator(login_required(login_url='/reviews/login'))
	@method_decorator(user_passes_test(is_manager,login_url='/reviews/unauthorized'))
	def dispatch(self, *args, **kwargs):
		return super(QuestionDetailView, self).dispatch(*args, **kwargs)