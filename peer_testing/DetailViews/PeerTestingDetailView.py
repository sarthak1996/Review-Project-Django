from django.views.generic.detail import DetailView
from peer_review.HelperClasses import StatusCodes,Timeline,CommonLookups,ApprovalTimeline
from peer_review.models import Review,Approval
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import user_passes_test,login_required
from configurations.HelperClasses.PermissionResolver import is_emp_or_manager
from configurations.HelperClasses import LoggingHelper
import traceback
class PeerTestingDetailView(DetailView):
	model=Review
	template_name='configurations/detail_view.html'
	context_object_name ='detail_obj'
	pk_url_kwarg='obj_pk'
	redirect_field_name = None
	login_url ='/reviews/login'

	def get_context_data(self, **kwargs):
		context=super(PeerTestingDetailView,self).get_context_data(**kwargs)
		logger=LoggingHelper(self.request.user,__name__)
		review_obj=self.object
		context['detail_view_card_title']='Peer testing'
		context['detail_name']=review_obj.bug_number
		context['name_first_letter']=context['detail_name'][0]
		context['detail_view_title']='Review'
		context['update_view_url']='peer_testing:peer_testing_update'
		context['button_label']='Update'
		context['update_rendered']=(review_obj.approval_outcome!=StatusCodes.get_approved_status() and review_obj.created_by==self.request.user)
		context['is_peer_test_active']='active'
		context['logged_in_user']=self.request.user
		context['created_by_user']=review_obj.created_by
		# context['delegate_rendered']=False
		# context['delegate_label']='Delegate'
		# context['delegate_view_url']='peer_review:delegate_review'
		context['invalidate_review']=(review_obj.approval_outcome==StatusCodes.get_pending_status())
		context['invlidate_view_url']='peer_review:invalidate_review'
		context['invalidate_label']='Invalidate'
		# exemptions=review_obj.exemption_review_assoc.all()
		# context['show_exemptions']=(exemptions.count()>0)
		# context['exemptions']=exemptions
		context['answer_rendered']=True
		approval_timeline=Approval.objects.filter(review=review_obj).all()
		approval_history=ApprovalTimeline.get_approval_timeline(review_obj,self.request)
		logger.write('\n'.join([str(usage) for usage in approval_history]),LoggingHelper.DEBUG)
		# context['right_aligned_timeline_title']='Approval History'
		context['right_aligned_timeline']=True
		context['approval_timeline']=approval_history
		context['approval_timeline_title']='Approval History'
		context['detail_view_type']='testing_review_user_view'
		logger.write('Context:'+str(context),LoggingHelper.DEBUG)
		return context



	@method_decorator(login_required(login_url='/reviews/login'))
	@method_decorator(user_passes_test(is_emp_or_manager,login_url='/reviews/unauthorized'))
	def dispatch(self, *args, **kwargs):
		return super(PeerTestingDetailView, self).dispatch(*args, **kwargs)


		