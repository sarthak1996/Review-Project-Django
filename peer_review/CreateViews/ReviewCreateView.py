from django.views.generic.edit import CreateView 
from peer_review.models import Review,Approval
import datetime 
from django.shortcuts import render,redirect
from peer_review.forms.ReviewForm import ReviewForm
from configurations.models import Question
from peer_review.HelperClasses import CommonLookups,StatusCodes,ApprovalHelper,PrintObjs,CommonValidations,EmailHelper
from django.db import transaction
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import user_passes_test,login_required
from configurations.HelperClasses.PermissionResolver import is_emp_or_manager

class ReviewCreateView(CreateView):
	model= Review
	form_class=ReviewForm
	template_name='configurations/create_view.html'
	redirect_field_name = None
	login_url ='/reviews/login'

	@transaction.atomic
	def form_valid(self, form):
		#create approval model and change latest of all the previous approval rows to false
		raised_to_user=get_user_model().objects.get(pk=form.cleaned_data['raise_to'].pk)
		review_obj=form.save(commit=False)
		if not CommonValidations.user_exists_in_team(raised_to_user,review_obj.team):
			form.add_error('raise_to','User '+str(raised_to_user.get_full_name())+' does not belong to the team to which the review was raised.')
			return super(ReviewCreateView,self).form_invalid(form)
		
		review_obj.last_update_by=self.request.user
		review_obj.created_by=self.request.user
		review_obj.creation_date=datetime.datetime.now()
		review_obj.review_type=CommonLookups.get_peer_review_question_type()
		# if not review_obj.num_of_exemption :
		# 	print('No exemptions entered')
		# 	review_obj.num_of_exemption=0
		print('Review approval:'+ review_obj.approval_outcome)
		PrintObjs.print_review_obj(review_obj)
		
		# review_obj.save()
		try:
			ApprovalHelper.mark_review_pending(review=review_obj,
							user=self.request.user,
							raised_to=form.cleaned_data['raise_to'])
		except Exception as e:
			form.add_error(None,str(e))
			handle_exception()
			return super(ReviewCreateView,self).form_invalid(form)

		EmailHelper.send_email(request=self.request,
							user=self.request.user,
							review=review_obj,
							is_updated=False)
		messages.success(self.request,'Review ' + review_obj.bug_number + ' sucessfully created - Pending approval')
		return redirect(review_obj.get_absolute_url())
		# return redirect(v)

	def get_context_data(self, **kwargs):
		context=super(ReviewCreateView,self).get_context_data(**kwargs)
		context['page_title']='Create Peer Review'
		context['card_title']='Peer Review'
		context['dependent_raise_to']=True
		context['is_review_active']='active'
		context['lov_raise_to_url']='peer_review:ajax_load_raise_to_lov'
		return context

	def get_form_kwargs(self):
		kw = super(ReviewCreateView, self).get_form_kwargs()
		kw['request'] = self.request
		return kw


	@method_decorator(login_required(login_url='/reviews/login'))
	@method_decorator(user_passes_test(is_emp_or_manager,login_url='/reviews/unauthorized'))
	def dispatch(self, *args, **kwargs):
		return super(ReviewCreateView, self).dispatch(*args, **kwargs)