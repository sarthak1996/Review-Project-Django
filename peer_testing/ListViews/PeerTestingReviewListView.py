from django.views.generic import ListView
from peer_review.models import Review
from peer_review.HelperClasses import StatusCodes,CommonLookups
class PeerTestingReviewListView(ListView):
	model=Review
	template_name='configurations/list_view.html'


	def get_context_data(self,**kwargs):
		context = super().get_context_data(**kwargs)
		context['create_url']='peer_testing:peer_testing_create_view'
		context['create_object_button_title']='Create Peer Testing'
		context['detail_view_url']='peer_testing:peer_testing_detail_view'
		context['page_title']='Peer Testing'
		context['create_button_rendered']=True
		return context

	def get_queryset(self):
		req=self.request 
		return Review.objects.filter(created_by=req.user,review_type=CommonLookups.get_peer_testing_question_type()).all()