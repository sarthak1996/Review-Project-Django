from django.views.generic.detail import DetailView
from peer_review.HelperClasses import StatusCodes
from peer_review.models import Review

class ReviewRaisedToMeDetailView(DetailView):
	model=Review
	template_name='configurations/detail_view.html'
	context_object_name ='detail_obj'
	pk_url_kwarg='obj_pk'

	def get_context_data(self, **kwargs):
		context=super(ReviewRaisedToMeDetailView,self).get_context_data(**kwargs)
		review_obj=self.object
		context['detail_view_card_title']='Review'
		context['detail_name']=review_obj.bug_number
		context['name_first_letter']=context['detail_name'][0]
		context['detail_view_title']='Review'
		context['update_view_url']='peer_review:review_update_view'
		context['button_label']='Approve'
		context['update_rendered']=(review_obj.approval_outcome==StatusCodes.get_pending_status())
		return context