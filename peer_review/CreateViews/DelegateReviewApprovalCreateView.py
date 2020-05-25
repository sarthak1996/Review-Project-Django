from django.views.generic.edit import CreateView 
from peer_review.models import Approval
from peer_review.forms.DelegateReviewApprovalFlowForm import DelegateReviewApprovalFlowForm
from django.db import transaction
from peer_review.HelperClasses import ApprovalHelper
from peer_review.models import Review
from django.shortcuts import render,redirect

class DelegateReviewApprovalCreateView(CreateView):
	model=Approval
	form_class=DelegateReviewApprovalFlowForm
	template_name='configurations/create_view.html'

	@transaction.atomic
	def form_valid(self, form):
		approval_instance=form.instance
		review_id=self.kwargs['review_obj']
		review=Review.objects.filter(pk=review_id).first()
		approval_instance.review=review
		if form.is_valid():
			ApprovalHelper.delegate_approval(review=review,
												user=self.request.user,
												raised_to=form.cleaned_data['raised_to'])
		return redirect('peer_review:review_home')


	def get_context_data(self, **kwargs):
		context=super(DelegateReviewApprovalCreateView,self).get_context_data(**kwargs)
		context['page_title']='Delegate Approval'
		context['card_title']='Delegate Approval'
		return context


	def get_form_kwargs(self):
		kw = super(DelegateReviewApprovalCreateView, self).get_form_kwargs()
		kw['request'] = self.request
		return kw