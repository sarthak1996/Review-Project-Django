from django.views.generic import ListView
from peer_review.models import Review,Approval
from peer_review.HelperClasses import StatusCodes,CommonLookups
class PeerTestingReviewRaisedToMeListView(ListView):
	model=Review
	template_name='configurations/list_view.html'
	# queryset=Approval.objects.filter(latest='True',raised_to=self.request.user).approval_review_assoc.all()
	def get_form_kwargs(self):
		kw = super(PeerTestingReviewRaisedToMeListView, self).get_form_kwargs()
		kw['request'] = self.request 
		return kw

	def get_context_data(self,**kwargs):
		context = super(PeerTestingReviewRaisedToMeListView,self).get_context_data(**kwargs)
		context['create_url']='peer_testing:peer_testing_create_view'
		context['create_object_button_title']='Create Peer Testing'
		context['detail_view_url']='peer_testing:peer_testing_approve_detail_view'
		context['page_title']='Peer Testing'
		context['create_button_rendered']=False
		# print()
		# print(Approval.objects.filter(latest='True',raised_to=self.request.user).approval_review_assoc.all())
		return context

	def get_queryset(self):
		return Review.objects.filter(approval_review_assoc__latest='True',approval_review_assoc__raised_to=self.request.user,approval_review_assoc__approval_outcome=StatusCodes.get_pending_status(),review_type=CommonLookups.get_peer_testing_question_type()).all()