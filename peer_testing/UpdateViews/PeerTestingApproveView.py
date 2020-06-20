from django.shortcuts import render,redirect
from peer_review.models import Review
from peer_review.HelperClasses import ApprovalHelper,EmailHelper
from django.views.generic.edit import UpdateView 
from peer_testing.forms.PeerTestingApprovalForm import PeerTestingApprovalForm
from django.db import transaction
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import user_passes_test,login_required
from configurations.HelperClasses.PermissionResolver import is_emp_or_manager,is_review_action_taker
from django.urls import reverse_lazy
class PeerTestingApproveView(UpdateView):
	model=Review
	template_name='configurations/create_view.html'
	# fields=[
	# 	'choice_text',
	# ]
	form_class=PeerTestingApprovalForm
	pk_url_kwarg='obj_pk'
	redirect_field_name = None
	login_url ='/reviews/login'

	def get_context_data(self, **kwargs):
		context=super(PeerTestingApproveView,self).get_context_data(**kwargs)
		context['page_title']='Approve Peer Testing'
		context['card_title']='Peer Testing'
		context['is_peer_test_active']='active'
		# context['dependent_raise_to']=True
		# context['lov_raise_to_url']='peer_review:ajax_load_raise_to_lov'
		return context

	@transaction.atomic
	def form_valid(self, form):
		review_instance=form.save(commit=False)
		review_instance.last_update_by = self.request.user
		
		ApprovalHelper.approve_review(review=review_instance,
										user=self.request.user,
										approver_comment=form.cleaned_data['approver_comment'])
		EmailHelper.send_email(request=self.request,
							user=self.request.user,
							review=review_instance,
							is_updated=False)
		messages.success(self.request,'Peer testing for '+review_instance.bug_number+ ' approved successfully!')
		return redirect('peer_testing:peer_testing_raised_to_me')



	@method_decorator(login_required(login_url='/reviews/login'))
	@method_decorator(user_passes_test(is_emp_or_manager,login_url='/reviews/unauthorized'))
	def dispatch(self, *args, **kwargs):
		if not is_review_action_taker(self.request.user,self.get_object()):
			return redirect(reverse_lazy('configurations:unauthorized_common'))
		return super(PeerTestingApproveView, self).dispatch(*args, **kwargs)
