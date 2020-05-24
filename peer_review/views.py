from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from peer_review.models import Approval,Review
from configurations.HelperClasses import ConfigurationDashboard
from peer_review.HelperClasses import PeerReviewApprovalQuestions,StatusCodes,ApprovalHelper
from peer_review.forms.PeerReviewAnswerForm import PeerReviewAnswerForm
from django.forms import modelformset_factory
from peer_testing.models import Answer
from datetime import datetime
from django.db import transaction
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

	initial_questions=PeerReviewApprovalQuestions.get_answer_form_sets_for_peer_review()
	model_formset=modelformset_factory(Answer, form=PeerReviewAnswerForm, extra=len(initial_questions))
	formset=model_formset(request.POST or None,queryset=Answer.objects.none(),initial=initial_questions)

	context_dict={}
	context_dict['formset']=formset
	context_dict['review_approval_title']='Approve Review'
	context_dict['detail_view_card_title']='Approval for Review'
	context_dict['detail_name']=review.bug_number
	context_dict['name_first_letter']=context_dict['detail_name'][0]
	context_dict['button_label']='Approve'
	
	# for form in formset:
	# 	print('Initial form values' + str(form.initial['question']))

	if request.method=='POST':
		all_forms_valid=False
		if formset.is_valid:
			# print('test')
			all_forms_valid=True
			for form in formset:
				print(form.errors)
				if form.is_valid():
					all_forms_valid=True
				else:
					all_forms_valid=False
					break
		print('Approval form :')
		print('Forms valid'+str(all_forms_valid))
		print('Formset errors (if any)')
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
				# print()
			formset.save()
			ApprovalHelper.approve_review(review)
			return redirect("peer_review:review_raised_to_me")
		# print('here')

	return render(request, 'peer_review/review_approval.html', context_dict)

