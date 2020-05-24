from django.views.generic import ListView
from peer_review.models import Review

class ReviewListView(ListView):
	model=Review
	template_name='configurations/list_view.html'


	def get_context_data(self,**kwargs):
		context = super().get_context_data(**kwargs)
		context['create_url']='peer_review:review_create_view'
		context['create_object_button_title']='Create Peer Review'
		context['detail_view_url']='peer_review:review_detail_view'
		context['page_title']='Peer Review'
		return context