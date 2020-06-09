from django.shortcuts import render,redirect
from peer_review.models import Review
from peer_review.HelperClasses import ApprovalHelper
from django.views.generic.edit import UpdateView 
from peer_testing.forms.PeerTestingApprovalForm import PeerTestingApprovalForm
from django.db import transaction
from django.contrib.auth.mixins import LoginRequiredMixin

class PeerTestingApproveView(LoginRequiredMixin,UpdateView):
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
		review_instance.created_by=self.request.user
		ApprovalHelper.approve_review(review_instance,self.request.user)
		return redirect('peer_testing:peer_testing_raised_to_me')
