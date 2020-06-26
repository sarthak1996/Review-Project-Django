from django.shortcuts import render,redirect
from peer_review.HelperClasses import CommonLookups
from peer_review.models import Approval,Review
from configurations.HelperClasses import ConfigurationDashboard
from peer_review.HelperClasses import StatusCodes,PrintObjs,ApprovalHelper,CommonValidations,EmailHelper
from peer_testing.HelperClasses import PeerTestingQuestions
from django.forms import modelformset_factory
from django.db import transaction
import datetime
from django.contrib import messages
from django.urls import reverse_lazy
from peer_testing.models import Answer
from peer_review.forms.PeerReviewAnswerForm import PeerReviewAnswerForm
from peer_testing.forms.PeerTestingReviewForm import PeerTestingReviewForm
from django.contrib.auth.decorators import login_required,user_passes_test
from configurations.HelperClasses.PermissionResolver import is_manager,is_emp_or_manager,is_review_raised_by_me,is_review_action_taker
from configurations.HelperClasses import LoggingHelper
import traceback
# Create your views here.

@login_required(login_url='/reviews/login')
@user_passes_test(is_emp_or_manager,login_url='/reviews/unauthorized')
def peer_testing_home(request):
	peer_testing_raised_by_me_count=request.user.reviews_created_by.all().filter(review_type=CommonLookups.get_peer_testing_question_type(),approval_outcome=StatusCodes.get_pending_status()).count()
	peer_testing_raised_to_me_count=Approval.objects.filter(latest='True',raised_to=request.user,approval_outcome=StatusCodes.get_pending_status(),review__review_type=CommonLookups.get_peer_testing_question_type()).all().count()
	
	dashboard_objects=[]
	raised_by_me_obj=ConfigurationDashboard('Raised by me','arrow_circle_up',peer_testing_raised_by_me_count,'peer_testing:peer_testing_list_view','image_floating_card_red','?filter_form-approval_outcome=PND')
	raised_to_me_obj=ConfigurationDashboard('Raised to me','arrow_circle_down',peer_testing_raised_to_me_count,'peer_testing:peer_testing_raised_to_me','image_floating_card_lime','?filter_form-approval_outcome=PND')
	dashboard_objects.append(raised_by_me_obj)
	dashboard_objects.append(raised_to_me_obj)
	context_dict={'dashboard_objects':dashboard_objects,'is_peer_test_active':'active'}
	return render(request,'configurations/configuration_home.html',context_dict)

@login_required(login_url='/reviews/login')
@user_passes_test(is_emp_or_manager,login_url='/reviews/unauthorized') 
def raise_peer_testing(request):
	initial_questions=PeerTestingQuestions.get_answer_form_sets_for_peer_testing(request)
	return create_or_update_review(request=request,
								initial_questions=initial_questions,
								initial_review_instance=None,
								edit=False)

@login_required(login_url='/reviews/login')
@user_passes_test(is_emp_or_manager,login_url='/reviews/unauthorized')
def update_peer_testing_review(request,**kwargs):
	review_id=kwargs['obj_pk']
	review=Review.objects.get(pk=review_id)
	if not is_review_raised_by_me(request.user,review):
		return redirect(reverse_lazy('configurations:unauthorized_common'))
	initial_answers=PeerTestingQuestions.construct_init_dictionary(review,request)
	
	return create_or_update_review(request=request,
		initial_questions=initial_answers,
		initial_review_instance=review,
		edit=True)

@login_required(login_url='/reviews/login')
@user_passes_test(is_emp_or_manager,login_url='/reviews/unauthorized')
@transaction.atomic
def create_or_update_review(request,initial_questions,initial_review_instance=None,edit=True):
	model_formset=modelformset_factory(Answer, form=PeerReviewAnswerForm, extra=len(initial_questions))
	formset=model_formset(request.POST or None,queryset=Answer.objects.none(),initial=initial_questions,prefix='answer')
	if initial_review_instance :
		review_form=PeerTestingReviewForm(request.POST or None,request=request,instance=initial_review_instance)
	else:
		review_form=PeerTestingReviewForm(request.POST or None,request=request)	
	context_dict={}
	context_dict['formset']=formset
	context_dict['review_approval_title']='Create Peer testing review'
	context_dict['detail_view_card_title']='Peer testing'
	context_dict['detail_name']='Peer testing'
	context_dict['name_first_letter']=context_dict['detail_name'][0]
	context_dict['button_label']='Submit'
	context_dict['review_form']=review_form
	context_dict['lov_raise_to_url']='peer_review:ajax_load_raise_to_lov'
	context_dict['dependent_raise_to']=True
	context_dict['is_peer_test_active']='active'
	review_pk=None
	logger=LoggingHelper(request.user,__name__)
	if edit and not initial_review_instance:
		logger.write('Invalid call ! returning with null',LoggingHelper.ERROR)
		return None
	if request.method=='POST':
		all_forms_valid=False
		if formset.is_valid:
			all_forms_valid=True
			for form in formset:
				logger.write('Review Form errors:')
				logger.write(str(form.errors),LoggingHelper.ERROR)
				if form.is_valid():
					all_forms_valid=True
				else:
					all_forms_valid=False
					break
		logger.write('Review form :',LoggingHelper.DEBUG)
		logger.write('Forms valid:'+str(all_forms_valid),LoggingHelper.DEBUG)
		logger.write('Review Formset errors (if any)',LoggingHelper.ERROR)
		logger.write(str(formset.errors),LoggingHelper.ERROR)
		logger.write(str(formset.non_form_errors()),LoggingHelper.ERROR)
		logger.write('Context:'+str(context_dict),LoggingHelper.DEBUG)
		if all_forms_valid:
			if review_form.is_valid():
				review_instance=review_form.save(commit=False)
				if not edit:
					review_instance.created_by=request.user
					review_instance.creation_date=datetime.datetime.now()
				review_instance.last_update_by=request.user
				review_instance.approval_outcome=StatusCodes.get_pending_status()
				review_instance.review_type=CommonLookups.get_peer_testing_question_type()
				PrintObjs.print_review_obj(review_instance,request.user)
				raised_to_user=review_form.cleaned_data['raise_to']
				if not CommonValidations.user_exists_in_team(raised_to_user,review_instance.team):
					form.add_error('raise_to','User '+str(raised_to_user.get_full_name())+' does not belong to the team to which the review was raised.')
					return render(request,'peer_testing/raise_peer_testing.html',context_dict)
				try:
					review_form.save()
				except Exception as e:
					review_form.add_error(None,str(e))
					logger.write('Exception occurred: '+ str(traceback.format_exc()),LoggingHelper.ERROR)
					handle_exception()
					return render(request,'peer_testing/raise_peer_testing.html',context_dict)
				review_pk=review_form.instance.pk
				if not edit:
					for form in formset:
						obj_instance=form.instance
						if 'question' in form.initial:
							obj_instance.question=form.initial['question']
						
						question_choice_type=obj_instance.question.question_choice_type
						obj_instance.answer=form.cleaned_data['single_choice_field'] if question_choice_type==CommonLookups.get_single_choice_question_type() else form.cleaned_data['text_answer']
						obj_instance.creation_date=datetime.datetime.now()
						obj_instance.created_by=request.user
						obj_instance.last_update_by=request.user
						obj_instance.review=review_instance
				else:
					for form in formset:
						obj_instance=form.instance
						if 'question' in form.initial:
							obj_instance.question=form.initial['question']
						answer_row=Answer.objects.get(review=initial_review_instance,question=obj_instance.question)
						question_choice_type=obj_instance.question.question_choice_type
						answer_row.answer=form.cleaned_data['single_choice_field'] if question_choice_type==CommonLookups.get_single_choice_question_type() else form.cleaned_data['text_answer']
						answer_row.last_update_by=request.user
						answer_row.review=review_instance
						try:
							answer_row.save()
						except Exception as e:
							form.add_error(None,str(e))
							logger.write('Exception occurred: '+ str(traceback.format_exc()),LoggingHelper.ERROR)
							handle_exception()
							return render(request,'peer_testing/raise_peer_testing.html',context_dict)

				
				try:
					ApprovalHelper.mark_review_pending(review=review_instance,
													user=request.user,
													request=request,
													raised_to=review_form.cleaned_data['raise_to'])
				except Exception as e:
					messages.error(request,str(e))
					logger.write('Exception occurred: '+ str(traceback.format_exc()),LoggingHelper.ERROR)
					handle_exception()
					return render(request,'peer_testing/raise_peer_testing.html',context_dict)
				if not edit:
					try:
						formset.save()
					except Exception as e:
						messages.error(request,str(e))
						logger.write('Exception occurred: '+ str(traceback.format_exc()),LoggingHelper.ERROR)
						handle_exception()
						return render(request,'peer_testing/raise_peer_testing.html',context_dict)
				EmailHelper.send_email(request=request,
							user=request.user,
							review=review_instance,
							is_updated=edit)
				if edit:
					messages.success(request,'Peer testing review '+review_instance.bug_number+' sucessfully updated!')
				else:
					messages.success(request,'Peer testing review '+review_instance.bug_number+' sucessfully raised!')
				return redirect(reverse_lazy('peer_testing:peer_testing_detail_view',kwargs={'obj_pk':review_pk}))
	return render(request,'peer_testing/raise_peer_testing.html',context_dict)



@login_required(login_url='/reviews/login')
@user_passes_test(is_emp_or_manager,login_url='/reviews/unauthorized')
def invalidate_peer_test(request,**kwargs):
	review_id=kwargs['obj_pk']
	review=Review.objects.filter(pk=review_id).first()
	if not is_review_raised_by_me(request.user,review):
		return redirect(reverse_lazy('configurations:unauthorized_common'))
	try:
		ApprovalHelper.invalidate_review(review,request.user,request)
	except Exception as e:
		messages.error(request,str(e))
		logger=LoggingHelper(request.user,__name__)
		logger.write('Exception occurred: '+ str(traceback.format_exc()),LoggingHelper.ERROR)
		handle_exception()
		return redirect(review.get_absolute_url())
	EmailHelper.send_email(request=request,
							user=request.user,
							review=review,
							is_updated=False)
	messages.success(request,'Review '+review.bug_number+' successfully invalidated!')
	return redirect(review.get_absolute_url())
