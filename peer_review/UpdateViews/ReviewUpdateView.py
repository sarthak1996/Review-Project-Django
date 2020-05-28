from django.views.generic.edit import UpdateView 
from peer_review.models import Review
from peer_review.forms.ReviewForm import ReviewForm
from peer_review.HelperClasses import CommonLookups,StatusCodes,ApprovalHelper
from django.db import transaction
from django.shortcuts import render,redirect
class ReviewUpdateView(UpdateView):
	model=Review
	template_name='configurations/create_view.html'
	# fields=[
	# 	'choice_text',
	# ]
	form_class=ReviewForm
	pk_url_kwarg='obj_pk'

	@transaction.atomic
	def form_valid(self, form):
		form.instance.last_update_by=self.request.user
		form.instance.review_type=CommonLookups.get_peer_review_question_type()
		review_obj=form.instance
		if form.is_valid():
			review_obj=form.save(commit=False)
			review_obj.approval_outcome=StatusCodes.get_pending_status()
			print('Review approval:'+ review_obj.approval_outcome)
			review_obj.save()
			ApprovalHelper.create_new_approval_row(review_obj=review_obj,
													user=self.request.user,
													raise_to=form.cleaned_data['raise_to'],
													approval_outcome=review_obj.approval_outcome,
													delegated=False)
			return redirect(review_obj.get_absolute_url())
		return redirect('peer_review:review_list_view')

	def get_context_data(self, **kwargs):
		context=super(ReviewUpdateView,self).get_context_data(**kwargs)
		context['page_title']='Update Peer Review'
		context['card_title']='Peer Review'
		return context
	def get_form_kwargs(self):
		kw = super(ReviewUpdateView, self).get_form_kwargs()
		kw['request'] = self.request
		return kw