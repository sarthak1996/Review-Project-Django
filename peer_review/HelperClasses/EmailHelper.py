import subprocess
from django.shortcuts import render
from django.contrib import messages
from peer_review.HelperClasses import ApprovalHelper, StatusCodes,CommonLookups
def send_email(request,user,review,is_updated=False):
	mail_dict=get_review_email_content(request,review,is_updated)
	print(mail_dict)
	if not mail_dict:
		print('Could not create mail dictionary for review: '+str(review))
		return
	to,cc=mail_dict['to'],mail_dict['cc']
	body,subject=mail_dict['body'],mail_dict['subject']
	
	if not review.email_subject or review.email_subject!=subject:
		review.email_subject=subject
		review.last_updated_by=user
		review.save()
	try:
		a = subprocess.check_call('echo "'+ 
									body +
									'" | mutt -e "set content_type=text/html" -s "'+subject+
									'"  '+to +' '
									+cc
									, shell=True,stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	except Exception as e:
		review.email_exceptions=str(e)
		review.last_updated_by=user
		review.save()
		print(e)
		messages.error(request,'Email could not be sent : '+e) #to check if custom error should be thrown
	messages.success(request,'Email has been sent')

def get_review_email_content(request,review,is_updated):
	latest_appr_row=ApprovalHelper.get_latest_approval_row(review)
	mail_dict={}
	mail_dict['subject']=get_mail_subject(review)
	if latest_appr_row.delegated:
		mail_dict['to']=latest_appr_row.raised_to.email
		mail_dict['cc']=' -c '+latest_appr_row.raised_by.email
		mail_dict['body']=get_delegated_review_body(request,review,latest_appr_row.raised_by)
		#send email to new raise_to mentioning old raised_to and review details
	elif latest_appr_row.approval_outcome==StatusCodes.get_pending_status():
		#send email to approver to approve
		mail_dict['to']=latest_appr_row.raised_to.email
		mail_dict['cc']=' -c '+review.created_by.email
		mail_dict['body']=get_pending_review_body(request,review,review.created_by,is_updated)
	elif latest_appr_row.approval_outcome==StatusCodes.get_invalid_status():
		#send email to approver - FYI review has been invalidated
		mail_dict['to']=latest_appr_row.raised_to.email
		mail_dict['cc']=' -c '+review.created_by.email
		mail_dict['body']=get_invalidated_review_body(request,review,review.created_by)
	elif latest_appr_row.approval_outcome==StatusCodes.get_approved_status():
		#send email to raised_by - FYI review has been approved
		mail_dict['to']=review.created_by.email
		mail_dict['cc']=' -c '+latest_appr_row.raised_to.email
		mail_dict['body']=get_approved_review_body(request,review,latest_appr_row.raised_to,latest_appr_row.approver_comment)
	elif latest_appr_row.approval_outcome==StatusCodes.get_rejected_status():
		#send email to raised_by - Action Required (review is rejected)
		mail_dict['to']=review.created_by.email
		mail_dict['cc']=' -c '+latest_appr_row.raised_to.email
		mail_dict['body']=get_rejected_review_body(request,review,latest_appr_row.raised_to,latest_appr_row.approver_comment)
	return mail_dict



	

def get_mail_subject(review):
	if review.review_type==CommonLookups.get_peer_review_question_type():
		return 'Mergereq checklist raised for review: '+review.bug_number
	elif review.review_type==CommonLookups.get_peer_testing_question_type():
		return 'Peer testing raised for review: '+review.bug_number

def get_delegated_review_body(request,review,delegated_by):
	string_response=str(get_outcome_complete_response(request=request,
								review=review,
								action='delegated',
								action_by=delegated_by).content.decode('utf-8'))
	# print(string_response)
	return string_response

def get_rejected_review_body(request,review,rejected_by,comment):
	string_response=str(get_outcome_complete_response(request=request,
								review=review,
								action='rejected',
								action_by=rejected_by,
								comment=comment).content.decode('utf-8'))
	# print(string_response)
	return string_response

def get_approved_review_body(request,review,approved_by,comment):
	string_response=str(get_outcome_complete_response(request=request,
								review=review,
								action='approved',
								action_by=approved_by,
								comment=comment).content.decode('utf-8'))
	# print(string_response)
	return string_response

def get_invalidated_review_body(request,review,invalidated_by):
	string_response=str(get_outcome_complete_response(request=request,
								review=review,
								action='invalidated',
								action_by=invalidated_by).content.decode('utf-8'))
	return string_response


def get_pending_review_body(request,review,action_by,is_updated):
	context={}
	context['review']=review
	context['action_by']=action_by
	context['is_updated']=is_updated
	context['peer_review']=True if review.review_type==CommonLookups.get_peer_review_question_type() else False
	context['high_priority']=True if review.priority == CommonLookups.get_review_high_priority() else False
	response=render(request,'email/pending_review_email.html',context)
	return str(response.content.decode('utf-8'))

def get_outcome_complete_response(request,review,action,action_by,comment=None):
	context={}
	context['review']=review
	context['action']=action
	context['high_priority']=True if review.priority == CommonLookups.get_review_high_priority() else False
	context['action_by']=action_by.get_full_name()
	context['comment']=comment
	context['peer_review']=True if review.review_type==CommonLookups.get_peer_review_question_type() else False
	response=render(request,'email/outcome_complete_review_email.html',context)
	
	return response
	

