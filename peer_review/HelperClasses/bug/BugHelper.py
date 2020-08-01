import cx_Oracle
import os
from django.contrib import messages
from peer_review.HelperClasses import CommonLookups,StatusCodes,ApprovalHelper
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
			error_code=cur.var(int)
			error_msg=cur.var(str)
			bug_text=get_bug_text_review(request,review)
			review.review_approved_checklist=bug_text
			review.save()
			if bug_text:
				cur.execute(get_pl_sql_to_update_bug(),
							bug_num=review.bug_number,
							bug_text=bug_text,
							error_code=error_code,
							error_msg=error_msg)
				con.commit()
				messages.error(request,error_msg.getvalue())
				logger.write('After bug update: '+str(error_code)+" -- "+str(error_msg),LoggingHelper.ERROR)
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
