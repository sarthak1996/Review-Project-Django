from django.views.generic.detail import DetailView
from peer_review.HelperClasses import StatusCodes,ApprovalTimeline,ApprovalHelper
from peer_review.models import Review
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import user_passes_test,login_required
from configurations.HelperClasses.PermissionResolver import is_emp_or_manager
from configurations.HelperClasses import LoggingHelper
import traceback

class ReviewRaisedToMeDetailView(DetailView):
	model=Review
	template_name='configurations/detail_view.html'
	context_object_name ='detail_obj'
	pk_url_kwarg='obj_pk'
	redirect_field_name = None
	login_url ='/reviews/login'

	def get_context_data(self, **kwargs):
		context=super(ReviewRaisedToMeDetailView,self).get_context_data(**kwargs)
		logger=LoggingHelper(self.request.user,__name__)
		review_obj=self.object
		context['detail_view_card_title']='Review'
		context['detail_name']=review_obj.bug_number
		context['name_first_letter']=context['detail_name'][0]
		context['detail_view_title']='Review'
		context['update_view_url']='peer_review:review_update_view'
		context['button_label']='Approve'
		context['update_rendered']=(review_obj.approval_outcome==StatusCodes.get_pending_status())
		context['delegate_rendered']=False
		context['delegate_label']='Delegate'
		context['delegate_view_url']='peer_review:delegate_view'
		context['invalidate_review']=False
		context['invlidate_view_url']='peer_review:invalidate_review'
		context['invalidate_label']='Invalidate'
		context['detail_view_type']='review_approval'
		context['is_review_active']='active'
		context['logged_in_user']=self.request.user
		context['created_by_user']=review_obj.created_by
		context['raised_to_user']=ApprovalHelper.get_latest_approval_row(review_obj,self.request).raised_to

		#approval timeline
		approval_timeline=Approval.objects.filter(review=review_obj).all()
		approval_history=ApprovalTimeline.get_approval_timeline(review_obj,self.request)
		logger.write('Preparing Approval timeline for review raised to me',LoggingHelper.DEBUG)
		logger.write('\n'.join([str(usage) for usage in approval_history]),LoggingHelper.DEBUG)
		
		context['right_aligned_timeline']=True
		context['approval_timeline']=approval_history
		context['approval_timeline_title']='Approval History'


		detail_timeline=Timeline(title=review.bug_number,
								description=[review.team.team_name],
								is_url=True,
								timeline_url='peer_review:review_detail_view',
								obj_pk=review.pk,
								request=self.request,
								title_right_floater=CommonLookups.get_priority_value(review.priority))
		context['detail_timeline']=[detail_timeline]
		context['detail_timeline_title']='Review details'
		logger.write('Context:'+str(context),LoggingHelper.DEBUG)

		return context



	@method_decorator(login_required(login_url='/reviews/login'))
	@method_decorator(user_passes_test(is_emp_or_manager,login_url='/reviews/unauthorized'))
	def dispatch(self, *args, **kwargs):
		return super(ReviewRaisedToMeDetailView, self).dispatch(*args, **kwargs)


		