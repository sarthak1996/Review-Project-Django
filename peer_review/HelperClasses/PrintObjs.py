from configurations.HelperClasses import LoggingHelper
import traceback

def print_approval_obj(approval_obj,request_user):
	logger=LoggingHelper(request_user,__name__)
	if not(approval_obj):
		logger.write('print_approval_obj(): Null is being passed to print! This should not happen.',LoggingHelper.ERROR)
		return
	logger.write('---Print Approval obj from start--',LoggingHelper.DEBUG)
	logger.write('Pk:',LoggingHelper.DEBUG)
	logger.write(str(approval_obj.pk),LoggingHelper.DEBUG)
	logger.write('Review pk:',LoggingHelper.DEBUG)
	logger.write(str(approval_obj.review.pk),LoggingHelper.DEBUG)
	logger.write('Raised by:',LoggingHelper.DEBUG)
	logger.write(str(approval_obj.raised_by),LoggingHelper.DEBUG)
	logger.write('Raised to:',LoggingHelper.DEBUG)
	logger.write(str(approval_obj.raised_to),LoggingHelper.DEBUG)
	logger.write('Approval outcome:',LoggingHelper.DEBUG)
	logger.write(str(approval_obj.approval_outcome),LoggingHelper.DEBUG)
	logger.write('Latest:',LoggingHelper.DEBUG)
	logger.write(str(approval_obj.latest),LoggingHelper.DEBUG)
	logger.write('Delegated:',LoggingHelper.DEBUG)
	logger.write(str(approval_obj.delegated),LoggingHelper.DEBUG)
	logger.write('---Print Approval obj end--',LoggingHelper.DEBUG)


def print_review_obj(review_obj,request_user):
	logger=LoggingHelper(request_user,__name__)
	if not(review_obj):
		logger.write('print_review_obj(): Null is being passed to print! This should not happen.',LoggingHelper.ERROR)
		return
	logger.write('---Print Review obj start--',LoggingHelper.DEBUG)
	logger.write('Pk:',LoggingHelper.DEBUG)
	logger.write(str(review_obj.pk),LoggingHelper.DEBUG)
	logger.write('Bug Number:',LoggingHelper.DEBUG)
	logger.write(str(review_obj.bug_number),LoggingHelper.DEBUG)
	logger.write('Approval outcome:',LoggingHelper.DEBUG)
	logger.write(str(review_obj.approval_outcome),LoggingHelper.DEBUG)
	logger.write('Team pk:',LoggingHelper.DEBUG)
	logger.write(str(review_obj.team.pk),LoggingHelper.DEBUG)
	logger.write('Review Type:',LoggingHelper.DEBUG)
	logger.write(str(review_obj.review_type),LoggingHelper.DEBUG)
	logger.write('---Print Review obj end--',LoggingHelper.DEBUG)


def print_exemption_obj(exemption_obj,request_user):
	logger=LoggingHelper(request_user,__name__)
	if not(exemption_obj):
		logger.write('print_exemption_obj(): Null is being passed to print! This should not happen.',LoggingHelper.DEBUG)
		return
	logger.write('---Print Exemption obj start--',LoggingHelper.DEBUG)
	logger.write('Pk:',LoggingHelper.DEBUG)
	logger.write(str(exemption_obj.pk),LoggingHelper.DEBUG)
	logger.write('Review pk',LoggingHelper.DEBUG)
	logger.write(str(exemption_obj.review.pk),LoggingHelper.DEBUG)
	logger.write('Exemption For',LoggingHelper.DEBUG)
	logger.write(str(exemption_obj.exemption_for),LoggingHelper.DEBUG)
	logger.write('Exemption explanation',LoggingHelper.DEBUG)
	logger.write(str(exemption_obj.exemption_explanation),LoggingHelper.DEBUG)
	logger.write('---Print Exemption obj end--',LoggingHelper.DEBUG)
