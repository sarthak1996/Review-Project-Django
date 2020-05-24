from peer_review.models import Review,Approval
from peer_review.HelperClasses import StatusCodes

def approve_review(review):
	latest_approval_row=get_latest_approval_row(review)
	status=StatusCodes.get_approved_status()
	change_status_approval_row(review,latest_approval_row,status)
	
def get_latest_approval_row(review):
	latest_approval_row=review.approval_review_assoc.filter(latest=True).all()
	if latest_approval_row.count()>1:
		print('Multiple rows exists for approval')
		raise Exception('Multiple latest rows exists for approval')
	if latest_approval_row.count()<0:
		print('No rows exists for approval')
		raise Exception('No latest rows exists for approval')
	if latest_approval_row.count()==1:
		return latest_approval_row.first()
	else:
		raise Exception('Error while fetching latest approval row.'+str(latest_approval_row.count()))

def change_status_approval_row(review,latest_approval_row,status):
	latest_approval_row.approval_outcome=status
	latest_approval_row.save()
	mark_rest_rows_as_not_latest(review,latest_approval_row)
	review.approval_outcome=status
	review.save()

def mark_rest_rows_as_not_latest(review,exclude):
	all_approval_rows=review.approval_review_assoc.all().exclude(pk=exclude.pk)
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

def delegate_review(review):
	pass



