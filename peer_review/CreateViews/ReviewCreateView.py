from django.views.generic.edit import CreateView 
from peer_review.models import Review,Approval
import datetime 
from peer_review.forms.ReviewForm import ReviewForm
from configurations.models import Question
from peer_review.HelperClasses import CommonLookups,StatusCodes,ApprovalHelper
from django.db import transaction
class ReviewCreateView(CreateView):
	model= Review
	form_class=ReviewForm
	template_name='configurations/create_view.html'

	@transaction.atomic
	def form_valid(self, form):
		form.instance.last_update_by=self.request.user
		form.instance.created_by=self.request.user
		form.instance.creation_date=datetime.datetime.now()
		form.instance.review_type=CommonLookups.get_peer_review_question_type()
		#create approval model and change latest of all the previous approval rows to false
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
		return super().form_valid(form)

	def get_context_data(self, **kwargs):
		context=super(ReviewCreateView,self).get_context_data(**kwargs)
		context['page_title']='Create Peer Review'
		context['card_title']='Peer Review'
		return context

	def get_form_kwargs(self):
		kw = super(ReviewCreateView, self).get_form_kwargs()
		kw['request'] = self.request
		return kw