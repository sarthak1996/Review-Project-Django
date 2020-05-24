from django.views.generic.edit import UpdateView 
from peer_review.models import Review
from peer_review.forms.ReviewForm import ReviewForm
class ReviewUpdateView(UpdateView):
	model=Review
	template_name='configurations/create_view.html'
	# fields=[
	# 	'choice_text',
	# ]
	form_class=ReviewForm
	pk_url_kwarg='obj_pk'

	def form_valid(self, form):
		form.instance.last_update_by=self.request.user
		form.instance.review_type='PRVW'
		return super().form_valid(form)

	def get_context_data(self, **kwargs):
		context=super(ReviewUpdateView,self).get_context_data(**kwargs)
		context['page_title']='Update Peer Review'
		context['card_title']='Peer Review'
		return context
	def get_form_kwargs(self):
		kw = super(ReviewUpdateView, self).get_form_kwargs()
		kw['request'] = self.request
		return kw