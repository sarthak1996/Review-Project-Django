from django.shortcuts import render,redirect
from peer_review.models import Review
from peer_review.HelperClasses import ApprovalHelper,EmailHelper
from django.views.generic.edit import UpdateView 
from peer_review.forms.ReviewRejectionForm import ReviewRejectionForm
from django.db import transaction
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import user_passes_test,login_required
from configurations.HelperClasses.PermissionResolver import is_emp_or_manager,is_review_action_taker
from django.contrib import messages
from configurations.HelperClasses import LoggingHelper
import traceback
class RejectReviewUpdateView(UpdateView):
	model=Review
	template_name='configurations/create_view.html'
	# fields=[
	# 	'choice_text',
	# ]
	form_class=ReviewRejectionForm
	pk_url_kwarg='obj_pk'
	redirect_field_name = None
	login_url ='/reviews/login'

	def get_context_data(self, **kwargs):
		context=super(RejectReviewUpdateView,self).get_context_data(**kwargs)
		context['page_title']='Reject Review'
		context['card_title']='Peer Review'
		context['is_review_active']='active'
		# context['dependent_raise_to']=True
		# context['lov_raise_to_url']='peer_review:ajax_load_raise_to_lov'
		return context

	@transaction.atomic
	def form_valid(self, form):
		
		review_instance=form.save(commit=False)
		# review_instance.save()
		try:
			ApprovalHelper.reject_review(review=review_instance,
										user=self.request.user,
										request=request,
										approver_comment=form.cleaned_data['approver_comment'])
		except Exception as e:
			form.add_error(None,str(e))
			logger=LoggingHelper(self.request.user,__name__)
			logger.write('Exception occurred: '+ str(traceback.format_exc()),LoggingHelper.ERROR)
			handle_exception()
			return super(RejectReviewUpdateView,self).form_invalid(form)

		EmailHelper.send_email(request=self.request,
							user=self.request.user,
							review=review_instance,
							is_updated=False)
		messages.success(self.request,'Review '+review_instance.bug_number+' sucessfully rejected!')
		return redirect('peer_review:review_raised_to_me')




	@method_decorator(login_required(login_url='/reviews/login'))
	@method_decorator(user_passes_test(is_emp_or_manager,login_url='/reviews/unauthorized'))
	def dispatch(self, *args, **kwargs):
		if not is_review_action_taker(self.request.user,self.get_object()):
			return redirect(reverse_lazy('configurations:unauthorized_common'))
		return super(RejectReviewUpdateView, self).dispatch(*args, **kwargs)
