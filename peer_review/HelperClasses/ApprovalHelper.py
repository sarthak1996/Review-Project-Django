from peer_review.models import Review,Approval
from peer_review.HelperClasses import StatusCodes
import datetime
def approve_review(review):
	latest_approval_row=get_latest_approval_row(review)
	status=StatusCodes.get_approved_status()
	change_status_approval_row(review,latest_approval_row,status)
	
def get_latest_approval_row(review,raise_exception=True):
	latest_approval_row=review.approval_review_assoc.filter(latest=True).all()
	if latest_approval_row.count()>1:
		print('Multiple rows exists for approval')
		if raise_exception:
			raise Exception('Multiple latest rows exists for approval')
	if latest_approval_row.count()<0:
		print('No rows exists for approval')
		if raise_exception:
			raise Exception('No latest rows exists for approval')
	if latest_approval_row.count()==1:
		return latest_approval_row.first()
	else:
		if raise_exception:
			raise Exception('Error while fetching latest approval row.'+str(latest_approval_row.count()))

def change_status_approval_row(review,latest_approval_row,status):
	latest_approval_row.approval_outcome=status
	latest_approval_row.save()
	mark_rest_rows_as_not_latest(review,latest_approval_row)
	review.approval_outcome=status
	review.save()

def mark_rest_rows_as_not_latest(review,exclude):
	all_approval_rows=get_all_approval_rows(review).exclude(pk=exclude.pk)
	all_approval_rows.update(latest=False)
	for apr in all_approval_rows:
		apr.save()

def reject_review(review):
	latest_approval_row=get_latest_approval_row(review)
	status=StatusCodes.get_rejected_status()
	change_status_approval_row(review,latest_approval_row,status)

def mark_review_pending(review):
	latest_approval_row=get_latest_approval_row(review)
	status=StatusCodes.get_pending_status()
	change_status_approval_row(review,latest_approval_row,status)

def get_all_approval_rows(review):
	return review.approval_review_assoc.all()

def delegate_approval(review,user,raised_to):
	create_new_approval_row(review_obj=review,
							user=user,
							raise_to=raised_to,
							approval_outcome=StatusCodes.get_pending_status(),
							delegated=True
							)

def mark_all_approval_rows_as_not_latest(all_approval_rows):
	all_approval_rows.update(latest=False)
	for apr in all_approval_rows:
		apr.save()

def create_new_approval_row(review_obj,user,raise_to,approval_outcome,delegated,is_create=False):
	if not is_create:
		latest_approval_row=get_latest_approval_row(review_obj,raise_exception=False)
		if latest_approval_row and latest_approval_row.approval_outcome==StatusCodes.get_approved_status():
			print('This should not have happened! - Approved rows should not have been touched from UI.')
			return
		if latest_approval_row:
			mark_all_approval_rows_as_not_latest(get_all_approval_rows(review_obj))
	approval_obj=Approval(review=review_obj,
								raised_by=user,
								raised_to=raise_to,
								approval_outcome=approval_outcome,
								delegated=delegated,
								latest=True,
								creation_date=datetime.datetime.now(),
								created_by=user,
								last_update_by=user)
	print('---Approval obj from create_new_approval_row start--')
	print('Pk:')
	print(approval_obj.pk)
	print('Review pk:')
	print(approval_obj.review.pk)
	print('Raised by:')
	print(approval_obj.raised_by)
	print('Raised to:')
	print(approval_obj.raised_to)
	print('Approval outcome:')
	print(approval_obj.approval_outcome)
	print('Latest:')
	print(approval_obj.latest)
	print('Delegated:')
	print(approval_obj.delegated)
	print('---Approval obj from create_new_approval_row end--')
	approval_obj.save()



