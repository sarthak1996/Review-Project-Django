from peer_review.HelperClasses import ApprovalHelper

from configurations.HelperClasses import LoggingHelper


def is_manager(user):
	if user:	
		logger=LoggingHelper(user,__name__)
		logger.write('Permission resolving as manager returned :'+str(user.groups.filter(name='Manager').count()>0),LoggingHelper.DEBUG)
		return user.groups.filter(name='Manager').count()>0
	return False

def is_employee(user):
	if user:
		logger=LoggingHelper(user,__name__)
		logger.write('Permission resolving as manager returned :'+str(user.groups.filter(name='Employee').count()>0),LoggingHelper.DEBUG)
		return user.groups.filter(name='Employee').count()>0
	return False

def is_emp_or_manager(user):
	return is_employee(user) or is_manager(user)

def is_review_action_taker(user,review):
	logger=LoggingHelper(user,__name__)
	latest_apr_row=ApprovalHelper.get_latest_approval_row(review,user)
	logger.write('Is review action taker permission resolver:'+str(latest_apr_row.raised_to==user),LoggingHelper.DEBUG)
	
	if latest_apr_row.raised_to!=user:
		return False
	return True

def is_review_raised_by_me(user,review):
	logger=LoggingHelper(user,__name__)
	logger.write('Is review raised by me permission resolver:'+str(review.created_by==user),LoggingHelper.DEBUG)
	return review.created_by==user
