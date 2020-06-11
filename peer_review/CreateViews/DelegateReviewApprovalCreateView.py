from django.views.generic.edit import CreateView 
from peer_review.models import Approval
from peer_review.forms.DelegateReviewApprovalFlowForm import DelegateReviewApprovalFlowForm
from django.db import transaction
from peer_review.HelperClasses import ApprovalHelper,CommonValidations
from peer_review.models import Review
from django.shortcuts import render,redirect
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import user_passes_test
from configurations.HelperClasses.PermissionResolver import is_emp_or_manager

class DelegateReviewApprovalCreateView(LoginRequiredMixin,CreateView):
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
		ApprovalHelper.delegate_approval(review=review,
											user=self.request.user,
											raised_to=form.cleaned_data['raised_to'])
		return redirect('peer_review:review_raised_to_me')
		
		# return redirect('peer_review:review_raised_to_me')
		# return super().form_valid(form)


	def get_context_data(self, **kwargs):
		context=super(DelegateReviewApprovalCreateView,self).get_context_data(**kwargs)
		context['page_title']='Delegate Approval'
		context['card_title']='Delegate Approval'
		context['is_review_active']='active'
		return context


	def get_form_kwargs(self):
		kw = super(DelegateReviewApprovalCreateView, self).get_form_kwargs()
		kw['request'] = self.request
		review_id=self.kwargs['obj_pk']
		review=Review.objects.filter(pk=review_id).first()
		kw['team_id'] = review.team.pk
		return kw


	@method_decorator(user_passes_test(is_emp_or_manager,login_url='/reviews/unauthorized'))
	def dispatch(self, *args, **kwargs):
		return super(DelegateReviewApprovalCreateView, self).dispatch(*args, **kwargs)