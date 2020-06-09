from django.shortcuts import render,redirect
from peer_review.HelperClasses import CommonLookups
from peer_review.models import Approval,Review
from configurations.HelperClasses import ConfigurationDashboard
from peer_review.HelperClasses import StatusCodes,PrintObjs,ApprovalHelper,CommonValidations
from peer_testing.HelperClasses import PeerTestingQuestions
from django.forms import modelformset_factory
from django.db import transaction
import datetime
from django.urls import reverse_lazy
from peer_testing.models import Answer
from peer_review.forms.PeerReviewAnswerForm import PeerReviewAnswerForm
from peer_testing.forms.PeerTestingReviewForm import PeerTestingReviewForm
# Create your views here.
def peer_testing_home(request):
	peer_testing_raised_by_me_count=request.user.reviews_created_by.all().filter(review_type=CommonLookups.get_peer_testing_question_type()).count()
	peer_testing_raised_to_me_count=Approval.objects.filter(latest='True',raised_to=request.user,approval_outcome=StatusCodes.get_pending_status(),review__review_type=CommonLookups.get_peer_testing_question_type()).all().count()
	
	dashboard_objects=[]
	raised_by_me_obj=ConfigurationDashboard('Raised by me','arrow_circle_up',peer_testing_raised_by_me_count,'peer_testing:peer_testing_list_view','image_floating_card_red','?filter_form-approval_outcome=PND')
	raised_to_me_obj=ConfigurationDashboard('Raised to me','arrow_circle_down',peer_testing_raised_to_me_count,'peer_testing:peer_testing_raised_to_me','image_floating_card_lime','?filter_form-approval_outcome=PND')
	dashboard_objects.append(raised_by_me_obj)
	dashboard_objects.append(raised_to_me_obj)
	context_dict={'dashboard_objects':dashboard_objects,'is_peer_test_active':'active'}
	return render(request,'configurations/configuration_home.html',context_dict)

@transaction.atomic 
def raise_peer_testing(request):
	initial_questions=PeerTestingQuestions.get_answer_form_sets_for_peer_testing()
	return create_or_update_review(request=request,
								initial_questions=initial_questions,
								initial_review_instance=None,
								edit=False)

@transaction.atomic
def update_peer_testing_review(request,**kwargs):
	review_id=kwargs['obj_pk']
	review=Review.objects.get(pk=review_id)
	initial_answers=PeerTestingQuestions.construct_init_dictionary(review)
	
	return create_or_update_review(request=request,
		initial_questions=initial_answers,
		initial_review_instance=review,
		edit=True)

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
	review_pk=None
	if edit and not initial_review_instance:
		print('Invalid call ! returning with null')
		return None
	if request.method=='POST':
		all_forms_valid=False
		if formset.is_valid:
			# print('test')
			all_forms_valid=True
			for form in formset:
				print('Review Form errors:')
				print(form.errors)
				if form.is_valid():
					all_forms_valid=True
				else:
					all_forms_valid=False
					break
		print('Review form :')
		print('Forms valid:'+str(all_forms_valid))
		print('Review Formset errors (if any)')
		print(formset.errors)
		print(formset.non_form_errors())

		if all_forms_valid:
			if review_form.is_valid:
				review_instance=review_form.save(commit=False)
				review_instance.created_by=request.user
				review_instance.creation_date=datetime.datetime.now()
				review_instance.last_update_by=request.user
				review_instance.approval_outcome=StatusCodes.get_pending_status()
				review_instance.review_type=CommonLookups.get_peer_testing_question_type()
				PrintObjs.print_review_obj(review_instance)
				raised_to_user=review_form.cleaned_data['raise_to']
				if not CommonValidations.user_exists_in_team(raised_to_user,review_instance.team):
					form.add_error('raise_to','User '+str(raised_to_user.get_full_name())+' does not belong to the team to which the review was raised.')
					return render(request,'peer_testing/raise_peer_testing.html',context_dict)
		
				review_form.save()
				review_pk=review_form.instance.pk
				if not edit:
					for form in formset:
						obj_instance=form.instance
						if 'question' in form.initial:
							obj_instance.question=form.initial['question']
						# print(obj_instance)
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
						answer_row.creation_date=datetime.datetime.now()
						answer_row.created_by=request.user
						answer_row.last_update_by=request.user
						answer_row.review=review_instance
						answer_row.save()

				
					
				if edit:
					ApprovalHelper.mark_review_pending(review=review_instance,user=request.user)
				else:
					ApprovalHelper.create_new_approval_row(review_obj=review_instance,
												user=request.user,
												raise_to=review_form.cleaned_data['raise_to'],
												approval_outcome=review_instance.approval_outcome,
												delegated=False,
												is_create=True)
				if not edit:
					formset.save()
			else:
				pass
			return redirect(reverse_lazy('peer_testing:peer_testing_detail_view',kwargs={'obj_pk':review_pk}))
	return render(request,'peer_testing/raise_peer_testing.html',context_dict)




