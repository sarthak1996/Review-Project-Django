from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from peer_review.models import Approval,Review,Exemption
from configurations.HelperClasses import ConfigurationDashboard
from peer_review.HelperClasses import PeerReviewApprovalQuestions,StatusCodes,ApprovalHelper,ExemptionHelper
from peer_review.forms.PeerReviewAnswerForm import PeerReviewAnswerForm
from peer_review.forms.ExemptionForm import ExemptionForm
from django.forms import modelformset_factory
from peer_testing.models import Answer
from datetime import datetime
from django.db import transaction
from peer_review.Formsets import RequiredFormSet
from configurations.models import Team
from collections import OrderedDict
# Create your views here.


def reviews_home(request):
	reviews_raised_by_me_count=request.user.reviews_created_by.all().count()
	reviews_raised_to_me_count=Approval.objects.filter(latest='True',raised_to=request.user,approval_outcome=StatusCodes.get_pending_status()).all().count()
	
	dashboard_objects=[]
	raised_by_me_obj=ConfigurationDashboard('Reviews Raised by me','',reviews_raised_by_me_count,'peer_review:review_list_view')
	raised_to_me_obj=ConfigurationDashboard('Reviews raised to me','',reviews_raised_to_me_count,'peer_review:review_raised_to_me')
	dashboard_objects.append(raised_by_me_obj)
	dashboard_objects.append(raised_to_me_obj)
	context_dict={'dashboard_objects':dashboard_objects}
	return render(request,'configurations/configuration_home.html',context_dict)

@transaction.atomic 
def peer_review_approval_form(request,**kwargs):
	# form=PeerReviewAnswerForm(request.POST or None)
	review_id=kwargs['obj_pk']
	review=Review.objects.filter(pk=review_id).first()

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
				obj_instance.review=review
				obj_instance.answer=form.cleaned_data['single_choice_field']
				obj_instance.creation_date=datetime.now()
				obj_instance.created_by=request.user
				obj_instance.last_update_by=request.user
				if 'question' in form.initial:
					obj_instance.question=form.initial['question']
				
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
				ApprovalHelper.approve_review(review,user)
				return redirect("peer_review:review_raised_to_me")
			print('Exemption Formset errors (if any)')
			print(exemption_formset.errors)
			print(exemption_formset.non_form_errors())
			
		# print('here')

	return render(request, 'peer_review/review_approval.html', context_dict)

def invalidate_review(request,**kwargs):
	review_id=kwargs['review_obj']
	review=Review.objects.filter(pk=review_id).first()
	ApprovalHelper.invalidate_review(review,request.user)
	return redirect(review.get_absolute_url())

def reject_review(request,**kwargs):
	review_id=kwargs['review_obj']
	review=Review.objects.filter(pk=review_id).first()
	ApprovalHelper.reject_review(review,request.user)
	return redirect(review.get_absolute_url())

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

