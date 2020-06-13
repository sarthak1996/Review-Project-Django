from django.views.generic.edit import UpdateView 
from peer_review.models import Review
from peer_review.forms.ReviewForm import ReviewForm
from peer_review.HelperClasses import CommonLookups,StatusCodes,ApprovalHelper,CommonValidations,EmailHelper
from django.db import transaction
from django.shortcuts import render,redirect
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import user_passes_test
from configurations.HelperClasses.PermissionResolver import is_emp_or_manager

class ReviewUpdateView(LoginRequiredMixin,UpdateView):
	model=Review
	template_name='configurations/create_view.html'
	# fields=[
	# 	'choice_text',
	# ]
	form_class=ReviewForm
	pk_url_kwarg='obj_pk'
	redirect_field_name = None
	login_url ='/reviews/login'

	@transaction.atomic
	def form_valid(self, form):
		raised_to_user=get_user_model().objects.get(pk=form.cleaned_data['raise_to'].pk)
		
		form.instance.last_update_by=self.request.user
		form.instance.review_type=CommonLookups.get_peer_review_question_type()
		review_obj=form.instance
		if not CommonValidations.user_exists_in_team(raised_to_user,review_obj.team):
			form.add_error('raise_to','User '+str(raised_to_user.get_full_name())+' does not belong to the team to which the review was raised.')
			return super(ReviewUpdateView,self).form_invalid(form)
		review_obj=form.save(commit=False)
		print('Review approval:'+ review_obj.approval_outcome)
		review_obj.save()
		ApprovalHelper.mark_review_pending(review=review_obj,
							user=self.request.user,
							raised_to=form.cleaned_data['raise_to'])
		EmailHelper.send_email(request=self.request,
							user=self.request.user,
							review=review_obj,
							is_updated=True)
		messages.success(self.request,'Review '+review_obj.bug_number+' Updated Sucessfully - Pending approval')
		return redirect(review_obj.get_absolute_url())
		

	def get_context_data(self, **kwargs):
		context=super(ReviewUpdateView,self).get_context_data(**kwargs)
		context['page_title']='Update Peer Review'
		context['card_title']='Peer Review'
		context['dependent_raise_to']=True
		context['lov_raise_to_url']='peer_review:ajax_load_raise_to_lov'
		context['is_review_active']='active'
		return context
	
	def get_form_kwargs(self):
		kw = super(ReviewUpdateView, self).get_form_kwargs()
		kw['request'] = self.request
		return kw



	@method_decorator(user_passes_test(is_emp_or_manager,login_url='/reviews/unauthorized'))
	def dispatch(self, *args, **kwargs):
		return super(ReviewUpdateView, self).dispatch(*args, **kwargs)
