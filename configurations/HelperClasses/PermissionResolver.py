from peer_review.HelperClasses import ApprovalHelper

def is_manager(user):
	if user:
		print('Permission resolving as manager returned :'+str(user.groups.filter(name='Manager').count()>0))
		return user.groups.filter(name='Manager').count()>0
	return False

def is_employee(user):
	if user:
		print('Permission resolving as manager returned :'+str(user.groups.filter(name='Employee').count()>0))
		return user.groups.filter(name='Employee').count()>0
	return False

def is_emp_or_manager(user):
	return is_employee(user) or is_manager(user)

def is_review_action_taker(user,review):
	latest_apr_row=ApprovalHelper.get_latest_approval_row(review)
	if latest_apr_row.raised_to!=user:
		return False
	return True

def is_review_raised_by_me(user,review):
	print('Is review raised by me permission resolver:')
	print(review.created_by==user)
	return review.created_by==user
