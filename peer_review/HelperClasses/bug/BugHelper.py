import cx_Oracle
import os
from django.contrib import messages
from peer_review.HelperClasses import CommonLookups,StatusCodes
from configurations.HelperClasses import LoggingHelper
import traceback
def get_pl_sql_to_update_bug():
	return """
		BEGIN
			bug.bug_api.create_bug_text
			(p_rptno		=> :bug_num,
			p_text			=> :bug_text,
			p_line_type		=> 'N',
			p_error_code	=> :error_code,
			p_error_mesg	=> :error_msg,
			p_hide			=> 'Y');
		END;
	"""

def update_bug(request,review):
	if review.review_type==CommonLookups.get_peer_review_question_type():
		logger=LoggingHelper(request.user,__name__)
		logger.write('Updating Bug text',LoggingHelper.DEBUG)
		try:
			connectString = os.getenv('ora_db_connect')
			con = cx_Oracle.connect(connectString)
			cur = con.cursor()
			error_code=cursor.var(int)
			error_msg=cursor.var(str)
			bug_text=get_bug_text_review(request,review)
			if bug_text:
				cur.execute(get_pl_sql_to_update_bug(),
							bug_num=review.bug_number,
							bug_text=bug_text,
							error_code=error_code,
							error_msg=out_error)
				if error_code or error_code.getvalue() or error_msg or error_msg.getvalue():
					messages.error(request,'Error while updating bug -' + str(error_code)+':'+str(error_msg))
					logger.write('Exception occurred: '+ str(traceback.format_exc()),LoggingHelper.ERROR)
				else:
					messages.success(request,'Bug updated sucessfully')
		except Exception as e:
			messages.error(request,str(e))
			logger.write('Exception occurred: '+ str(traceback.format_exc()),LoggingHelper.ERROR)

def get_bug_text_review(request,review):
	answers=review.answer_review_assoc.all()
	latest_approval_row=ApprovalHelper.get_latest_approval_row(review,request.user)
	if latest_approval_row.approval_outcome != StatusCodes.get_approved_status():
		messages.error(request,'Latest status is not approved!!! This should not have happened..')
		return None
	approver=latest_approval_row.raised_to
	text='---Mergereq checklist validated by '+approver.get_full_name()+'---\n'
	for answer in answers:
		text+='\t- '+answer.question.question_text\
				+' : '+answer.answer + '\n' 
	exemptions=review.exemption_review_assoc.all()
	text+='---Exemptions---\n'
	for exemption in exemptions:
		text+='\t- '+exemption.exemption_for\
				+' : '+exemption.exemption_explanation+'\n'
	return text
