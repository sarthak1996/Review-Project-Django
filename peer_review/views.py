from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from peer_review.models import Approval,Review,Exemption
from configurations.HelperClasses import ConfigurationDashboard
from peer_review.HelperClasses import PeerReviewApprovalQuestions,StatusCodes,ApprovalHelper,ExemptionHelper,CommonLookups,Timeline,EmailHelper
from peer_review.forms.PeerReviewAnswerForm import PeerReviewAnswerForm
from peer_review.forms.ExemptionForm import ExemptionForm
from django.forms import modelformset_factory
from peer_testing.models import Answer
from datetime import datetime
from django.db import transaction
from peer_review.Formsets import RequiredFormSet
from configurations.models import Team
from collections import OrderedDict
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required,user_passes_test
from configurations.HelperClasses.PermissionResolver import is_manager,is_emp_or_manager,is_review_action_taker

# Create your views here.

@login_required(login_url='/reviews/login')
@user_passes_test(is_emp_or_manager,login_url='/reviews/unauthorized')
def reviews_home(request):
	reviews_raised_by_me_count=request.user.reviews_created_by.all().filter(review_type=CommonLookups.get_peer_review_question_type()).count()
	reviews_raised_to_me_count=Approval.objects.filter(latest='True',raised_to=request.user,approval_outcome=StatusCodes.get_pending_status(),review__review_type=CommonLookups.get_peer_review_question_type()).all().count()
	
	dashboard_objects=[]
	raised_by_me_obj=ConfigurationDashboard('Raised by me','arrow_circle_up',reviews_raised_by_me_count,'peer_review:review_list_view','image_floating_card_red','?filter_form-approval_outcome=PND')
	raised_to_me_obj=ConfigurationDashboard('Raised to me','arrow_circle_down',reviews_raised_to_me_count,'peer_review:review_raised_to_me','image_floating_card_lime','?filter_form-approval_outcome=PND')
	dashboard_objects.append(raised_by_me_obj)
	dashboard_objects.append(raised_to_me_obj)
	context_dict={'dashboard_objects':dashboard_objects,'is_review_active':'active'}
	return render(request,'configurations/configuration_home.html',context_dict)

@login_required(login_url='/reviews/login')
@user_passes_test(is_emp_or_manager,login_url='/reviews/unauthorized')
@transaction.atomic 
def peer_review_approval_form(request,**kwargs):
	# form=PeerReviewAnswerForm(request.POST or None)
	review_id=kwargs['obj_pk']
	review=Review.objects.filter(pk=review_id).first()
	if not is_review_action_taker(request.user,review):
		return redirect(reverse_lazy('configurations:unauthorized_common'))
	initial_questions=PeerReviewApprovalQuestions.get_answer_form_sets_for_peer_review(review)
	model_formset=modelformset_factory(Answer, form=PeerReviewAnswerForm, extra=len(initial_questions))
	formset=model_formset(request.POST or None,queryset=Answer.objects.none(),initial=initial_questions,prefix='answer')
	
	exemption_model_fs=modelformset_factory(Exemption, form=ExemptionForm, extra=0,can_delete=True,formset=RequiredFormSet)
	exemption_formset=exemption_model_fs(request.POST or None,queryset=Exemption.objects.none(),prefix='exemption')
	context_dict={}
	context_dict['formset']=formset
	context_dict['exemption_formset']=exemption_formset
	context_dict['review_approval_title']='Approve Review'
	context_dict['detail_view_card_title']='Approval for Review'
	context_dict['detail_name']=review.bug_number
	context_dict['name_first_letter']=context_dict['detail_name'][0]
	context_dict['button_label']='Approve'
	context_dict['review_object']=review
	context_dict['is_review_active']='active'
	context_dict['logged_in_user']=request.user
	context_dict['created_by_user']=review.created_by
	context_dict['raised_to_user']=ApprovalHelper.get_latest_approval_row(review).raised_to
	
	#approval timeline
	approval_timeline=Approval.objects.filter(review=review).all()
	approval_history=[]
	for approval in approval_timeline:
		approval_history.append(Timeline(title=approval.raised_to.get_full_name(),
										description=approval.approver_comment,
										is_url=False,
										title_right_floater=CommonLookups.get_approval_value(approval.approval_outcome)
										))
	print('\n'.join([str(usage) for usage in approval_history]))
	context_dict['right_aligned_timeline']=True

	context_dict['right_aligned_timeline']=True
	context_dict['approval_timeline']=approval_history
	context_dict['approval_timeline_title']='Approval History'


	detail_timeline=Timeline(title=review.bug_number,
							description=['Team: '+ review.team.team_name,'Series type: '+CommonLookups.get_series_type_value(review.series_type),'Raised by: '+review.created_by.get_full_name()],
							is_url=True,
							timeline_url='peer_review:review_detail_view',
							obj_pk=review.pk,
							title_right_floater=CommonLookups.get_priority_value(review.priority))
	context_dict['detail_timeline']=[detail_timeline]
	context_dict['detail_timeline_title']='Review details'
	# for form in formset:
	# 	print('Initial form values' + str(form.initial['question']))

	if request.method=='POST':
		all_forms_valid=False
		if formset.is_valid:
			# print('test')
			all_forms_valid=True
			for form in formset:
				print('Approval Form errors:')
				print(form.errors)
				if form.is_valid():
					all_forms_valid=True
				else:
					all_forms_valid=False
					break
		print('Approval form :')
		print('Forms valid:'+str(all_forms_valid))
		print('Review Approval Formset errors (if any)')
		print(formset.errors)
		print(formset.non_form_errors())
		if all_forms_valid:
			# print('here2')
			for form in formset:

				obj_instance=form.instance
				if 'question' in form.initial:
					obj_instance.question=form.initial['question']
				question_choice_type=obj_instance.question.question_choice_type
				obj_instance.review=review
				obj_instance.answer=form.cleaned_data['single_choice_field'] if question_choice_type==CommonLookups.get_single_choice_question_type() else form.cleaned_data['text_answer']
				obj_instance.creation_date=datetime.now()
				obj_instance.created_by=request.user
				obj_instance.last_update_by=request.user
				
				
			print('Exemption logging')
			all_forms_valid=False
			if exemption_formset.is_valid():
				all_forms_valid=True
				print('Exemption formset is valid')
				print('Printing exemption form details')
				for form1 in exemption_formset:
					print('Exemption Form errors:')
					print(form1.errors)
					if form1.is_valid():
						all_forms_valid=True
					else:
						all_forms_valid=False
						break
			print('Exemption form:')
			print('Forms valid:'+str(all_forms_valid))
			# print('Request')
			# print(request.POST)
			if all_forms_valid:
				for form1 in exemption_formset:

					
					obj_instance=form1.instance
					if not form1.cleaned_data.get('DELETE',False):
						# print(form1.cleaned_data)
						exemption_for=form1.cleaned_data['exemption_for']
						exemption_explanation=form1.cleaned_data['exemption_explanation']
						ExemptionHelper.create_exemption_row(review=review,
															user=request.user,
															exemption_for=exemption_for,
															exemption_explanation=exemption_explanation
															)
				#save answer model from formset
				formset.save()
				ApprovalHelper.approve_review(review=review,
											user=request.user,
											approver_comment=None)
				EmailHelper.send_email(request=request,
							user=request.user,
							review=review,
							is_updated=False)
				messages.success(request,'Review '+review.bug_number+' successfully approved!')
				return redirect("peer_review:review_raised_to_me")
			print('Exemption Formset errors (if any)')
			print(exemption_formset.errors)
			print(exemption_formset.non_form_errors())
			
		# print('here')

	return render(request, 'peer_review/review_approval.html', context_dict)



@login_required(login_url='/reviews/login')
@user_passes_test(is_emp_or_manager,login_url='/reviews/unauthorized')
def invalidate_review(request,**kwargs):
	review_id=kwargs['obj_pk']
	review=Review.objects.filter(pk=review_id).first()
	if not is_review_action_taker(request.user,review):
		return redirect(reverse_lazy('configurations:unauthorized_common'))
	ApprovalHelper.invalidate_review(review,request.user)
	EmailHelper.send_email(request=request,
							user=request.user,
							review=review,
							is_updated=False)
	messages.success(request,'Review '+review.bug_number+' successfully invalidated!')
	return redirect(review.get_absolute_url())

# @login_required(login_url='/reviews/login')
# @user_passes_test(is_emp_or_manager,login_url='/reviews/unauthorized')
# def reject_review(request,**kwargs):
# 	review_id=kwargs['obj_pk']
# 	review=Review.objects.filter(pk=review_id).first()
# 	ApprovalHelper.reject_review(review,request.user)-->to create cbv to cpture comment
# 	return redirect(review.get_absolute_url())

@login_required(login_url='/reviews/login')
@user_passes_test(is_emp_or_manager,login_url='/reviews/unauthorized')
def load_users_based_on_team(request):
	# review=request.GET.get('review')
	# print('Review request url')
	# print(request.GET)
	team=request.GET.get('team')
	print('Team id:'+str(team))
	team_obj=Team.objects.get(pk=team)
	print(team_obj)
	users=team_obj.user_team_assoc.all().exclude(pk=request.user.pk).order_by('first_name')
	objects_lov=OrderedDict()
	for user in users:
		objects_lov[user.pk]=user.get_full_name()
	return render(request,'lov/dependent_lov.html',{'objects':objects_lov.items()})

