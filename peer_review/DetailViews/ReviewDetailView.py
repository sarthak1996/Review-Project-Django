from django.views.generic.detail import DetailView
from peer_review.HelperClasses import StatusCodes,Timeline,CommonLookups,ApprovalTimeline
from peer_review.models import Review,Approval,Exemption
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import user_passes_test
from configurations.HelperClasses.PermissionResolver import is_emp_or_manager

class ReviewDetailView(LoginRequiredMixin,DetailView):
	model=Review
	template_name='configurations/detail_view.html'
	context_object_name ='detail_obj'
	pk_url_kwarg='obj_pk'
	redirect_field_name = None
	login_url ='/reviews/login'

	def get_context_data(self, **kwargs):
		context=super(ReviewDetailView,self).get_context_data(**kwargs)
		review_obj=self.object
		context['detail_view_card_title']='Review'
		context['detail_name']=review_obj.bug_number
		context['name_first_letter']=context['detail_name'][0]
		context['detail_view_title']='Review'
		context['update_view_url']='peer_review:review_update_view'
		context['button_label']='Update'
		context['update_rendered']=(review_obj.approval_outcome!=StatusCodes.get_approved_status() and review_obj.created_by==self.request.user)
		context['delegate_rendered']=False
		context['delegate_label']='Delegate'
		context['delegate_view_url']='peer_review:delegate_review'
		context['invalidate_review']=(review_obj.approval_outcome==StatusCodes.get_pending_status())
		context['invlidate_view_url']='peer_review:invalidate_review'
		context['invalidate_label']='Invalidate'
		exemptions=review_obj.exemption_review_assoc.all()
		context['show_exemptions']=(exemptions.count()>0)
		context['exemptions']=exemptions
		context['detail_view_type']='review_user_view'
		context['is_review_active']='active'
		context['logged_in_user']=self.request.user
		context['created_by_user']=review_obj.created_by
		
		#approval timeline
		approval_timeline=Approval.objects.filter(review=review_obj).all()
		approval_history=ApprovalTimeline.get_approval_timeline(review_obj)
		print('\n'.join([str(usage) for usage in approval_history]))
		

		context['right_aligned_timeline']=True
		context['approval_timeline']=approval_history
		context['approval_timeline_title']='Approval History'


		exemptions_added=Exemption.objects.filter(review=review_obj).all()
		exemption_timeline=[]
		for exemption in exemptions_added:
			exemption_timeline.append(Timeline(title=exemption.exemption_for,
												description=exemption.exemption_explanation,
												is_url=False))
		context['exemption_timeline']=exemption_timeline
		context['exemption_timeline_title']='Exemptions granted'



		return context


	@method_decorator(user_passes_test(is_emp_or_manager,login_url='/reviews/unauthorized'))
	def dispatch(self, *args, **kwargs):
		return super(ReviewDetailView, self).dispatch(*args, **kwargs)

