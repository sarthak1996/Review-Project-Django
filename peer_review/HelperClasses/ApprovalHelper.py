from peer_review.models import Review,Approval
from peer_review.HelperClasses import StatusCodes
def approve_review(review):
	latest_approved_row=review.approval_review_assoc.filter(latest=True).all()
	if latest_approved_row.count()>1:
		print('Multiple rows exists for approval')
		raise Exception('Multiple latest rows exists for approval')
	if latest_approved_row.count()<0:
		print('No rows exists for approval')
		raise Exception('No latest rows exists for approval')
	if latest_approved_row.count()==1:
		latest_approved_row=latest_approved_row.first()
		latest_approved_row.approval_outcome=StatusCodes.get_approved_status()
		latest_approved_row.save()
		mark_rest_rows_as_not_latest(review,latest_approved_row)
		review.approval_outcome=StatusCodes.get_approved_status()
		review.save()
	

def mark_rest_rows_as_not_latest(review,exclude):
	all_approval_rows=review.approval_review_assoc.all().exclude(pk=exclude.pk)
	all_approval_rows.update(latest=False)
	for apr in all_approval_rows:
		apr.save()
