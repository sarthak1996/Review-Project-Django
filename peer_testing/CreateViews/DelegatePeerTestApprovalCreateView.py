from django.views.generic.edit import CreateView 
from peer_review.models import Approval
from peer_review.forms.DelegateReviewApprovalFlowForm import DelegateReviewApprovalFlowForm
from django.db import transaction
from peer_review.HelperClasses import ApprovalHelper,CommonValidations,EmailHelper
from peer_review.models import Review
from django.shortcuts import render,redirect
from django.contrib.auth import get_user_model
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.urls import reverse_lazy
from django.contrib.auth.decorators import user_passes_test,login_required
from configurations.HelperClasses.PermissionResolver import is_emp_or_manager,is_review_action_taker
from configurations.HelperClasses import LoggingHelper
import traceback
class DelegatePeerTestApprovalCreateView(CreateView):
	model=Approval
	form_class=DelegateReviewApprovalFlowForm
	template_name='configurations/create_view.html'
	redirect_field_name = None
	login_url ='/reviews/login'

	@transaction.atomic
	def form_valid(self, form):
		approval_instance=form.instance
		review_id=self.kwargs['obj_pk']
		review=Review.objects.filter(pk=review_id).first()
		
		approval_instance.review=review
		raised_to_user=get_user_model().objects.get(pk=form.cleaned_data['raised_to'].pk)
		if not CommonValidations.user_exists_in_team(raised_to_user,review.team):
			form.add_error('raised_to','User '+str(raised_to_user.get_full_name())+' does not belong to the team to which the review was raised.')
			return super(DelegateReviewApprovalCreateView,self).form_invalid(form)
		try:
			ApprovalHelper.delegate_approval(review=review,
											user=self.request.user,
											request=self.request,
											raised_to=form.cleaned_data['raised_to'])
		except Exception as e:
			form.add_error(None,str(e))
			logger=LoggingHelper(self.request.user,__name__)
			logger.write('Exception occurred: '+ str(traceback.format_exc()),LoggingHelper.ERROR)
			
			handle_exception()
			return super(DelegatePeerTestApprovalCreateView,self).form_invalid(form)
		EmailHelper.send_email(request=request,
							user=self.request.user,
							review=review,
							is_updated=False)
		messages.success(self.request,'Review '+review.bug_number+' sucessfully delegated!')
		return redirect('peer_review:review_raised_to_me')
		
		# return redirect('peer_review:review_raised_to_me')
		# return super().form_valid(form)


	def get_context_data(self, **kwargs):
		context=super(DelegatePeerTestApprovalCreateView,self).get_context_data(**kwargs)
		context['page_title']='Delegate Approval'
		context['card_title']='Delegate Approval'
		context['is_peer_test_active']='active'
		return context


	def get_form_kwargs(self):
		kw = super(DelegatePeerTestApprovalCreateView, self).get_form_kwargs()
		kw['request'] = self.request
		review_id=self.kwargs['obj_pk']
		review=Review.objects.filter(pk=review_id).first()
		kw['team_id'] = review.team.pk
		return kw


	@method_decorator(login_required(login_url='/reviews/login'))
	@method_decorator(user_passes_test(is_emp_or_manager,login_url='/reviews/unauthorized'))
	def dispatch(self, *args, **kwargs):
		review_id=self.kwargs['obj_pk']
		review=Review.objects.filter(pk=review_id).first()
		if not is_review_action_taker(self.request.user,review):
			return redirect(reverse_lazy('configurations:unauthorized_common'))
		return super(DelegatePeerTestApprovalCreateView, self).dispatch(*args, **kwargs)