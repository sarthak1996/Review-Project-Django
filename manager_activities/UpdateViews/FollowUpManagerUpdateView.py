from django.shortcuts import render,redirect
from peer_review.models import Review
from peer_review.HelperClasses import ApprovalHelper,EmailHelper
from django.views.generic.edit import UpdateView 
from peer_review.forms.ReviewRejectionForm import ReviewRejectionForm
from django.db import transaction
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import user_passes_test,login_required
from configurations.HelperClasses.PermissionResolver import is_emp_or_manager
from django.contrib import messages
from peer_review.forms.FollowUpForm import FollowUpForm

class FollowUpManagerUpdateView(UpdateView):
	model=Review
	template_name='configurations/create_view.html'
	# fields=[
	# 	'choice_text',
	# ]
	form_class=FollowUpForm
	pk_url_kwarg='obj_pk'

	def get_context_data(self, **kwargs):
		context=super(FollowUpManagerUpdateView,self).get_context_data(**kwargs)
		context['page_title']='Follow Up Review'
		context['card_title']='Follow Up Review'
		context['is_man_home_active']='active'
		# context['dependent_raise_to']=True
		# context['lov_raise_to_url']='peer_review:ajax_load_raise_to_lov'
		return context

	@transaction.atomic
	def form_valid(self, form):
		review_instance=form.save(commit=False)
		review_instance.last_update_by = self.request.user
		# review_instance.save()
		latest_apr_row=ApprovalHelper.get_latest_approval_row(review_instance)
		try:
			ApprovalHelper.mark_review_pending(review=review_instance,
												user=self.request.user,
												raised_to=latest_apr_row.raised_to,
												comment=form.cleaned_data['approver_comment'])
		except Exception as e:
			form.add_error(None,str(e))
			handle_exception()
			return super(FollowUpManagerUpdateView,self).form_invalid(form)
		EmailHelper.send_email(request=self.request,
								user=self.request.user,
								review=review_instance,
								is_updated=False,
								follow_up=True)
		return redirect('manager_activities:peer_testing_raised_to_me')




	@method_decorator(login_required(login_url='/reviews/login'))
	@method_decorator(user_passes_test(is_emp_or_manager,login_url='/reviews/unauthorized'))
	def dispatch(self, *args, **kwargs):
		return super(FollowUpManagerUpdateView, self).dispatch(*args, **kwargs)
