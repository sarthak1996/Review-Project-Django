from django.views.generic.detail import DetailView
from peer_review.HelperClasses import StatusCodes,Timeline,CommonLookups,ApprovalTimeline
from peer_review.models import Review,Approval,Exemption
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import user_passes_test,login_required
from configurations.HelperClasses.PermissionResolver import is_manager
from configurations.HelperClasses import LoggingHelper
import traceback

class PeerReviewManagerDetailView(DetailView):
	model=Review
	template_name='configurations/detail_view.html'
	context_object_name ='detail_obj'
	pk_url_kwarg='obj_pk'
	redirect_field_name = None
	login_url ='/reviews/login'

	def get_context_data(self, **kwargs):
		context=super(PeerReviewManagerDetailView,self).get_context_data(**kwargs)
		logger=LoggingHelper(self.request.user,__name__)
		review_obj=self.object
		context['detail_view_card_title']='Review'
		context['detail_name']=review_obj.bug_number
		context['name_first_letter']=context['detail_name'][0]
		context['detail_view_title']='Review - Manager'
		
		exemptions=review_obj.exemption_review_assoc.all()
		context['show_exemptions']=(exemptions.count()>0)
		context['exemptions']=exemptions
		context['detail_view_type']='manager_view_review'
		context['is_man_home_active']='active'
		context['logged_in_user']=self.request.user
		context['created_by_user']=review_obj.created_by
		
		#approval timeline
		approval_timeline=Approval.objects.filter(review=review_obj).all()
		approval_history=ApprovalTimeline.get_approval_timeline(review_obj,request=self.request)
		logger.write('\n'.join([str(usage) for usage in approval_history]),LoggingHelper.DEBUG)
		

		context['right_aligned_timeline']=True
		context['approval_timeline']=approval_history
		context['approval_timeline_title']='Approval History'


		exemptions_added=Exemption.objects.filter(review=review_obj).all()
		exemption_timeline=[]
		for exemption in exemptions_added:
			exemption_timeline.append(Timeline(title=exemption.exemption_for,
												description=exemption.exemption_explanation,
												is_url=False,
												request=self.request))
		context['exemption_timeline']=exemption_timeline
		context['exemption_timeline_title']='Exemptions granted'

		logger.write('Context:'+str(context),LoggingHelper.DEBUG)

		return context


	@method_decorator(login_required(login_url='/reviews/login'))
	@method_decorator(user_passes_test(is_manager,login_url='/reviews/unauthorized'))
	def dispatch(self, *args, **kwargs):
		return super(PeerReviewManagerDetailView, self).dispatch(*args, **kwargs)

