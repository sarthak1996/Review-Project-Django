from django.shortcuts import render,redirect
from peer_review.models import Review
from peer_review.HelperClasses import ApprovalHelper
from django.views.generic.edit import UpdateView 
from peer_review.forms.ReviewRejectionForm import ReviewRejectionForm
from django.db import transaction
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import user_passes_test
from configurations.HelperClasses.PermissionResolver import is_emp_or_manager

class RejectReviewUpdateView(LoginRequiredMixin,UpdateView):
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
		review_instance.last_update_by = self.request.user
		review_instance.save()
		ApprovalHelper.reject_review(review=review_instance,
										user=self.request.user,
										approver_comment=form.cleaned_data['approver_comment'])
		
		return redirect('peer_review:review_raised_to_me')




	@method_decorator(user_passes_test(is_emp_or_manager,login_url='/reviews/unauthorized'))
	def dispatch(self, *args, **kwargs):
		return super(RejectReviewUpdateView, self).dispatch(*args, **kwargs)
