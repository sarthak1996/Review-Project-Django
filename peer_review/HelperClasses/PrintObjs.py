def print_approval_obj(approval_obj):
	if not(approval_obj):
		print('print_approval_obj(): Null is being passed to print! This should not happen.')
		return
	print('---Print Approval obj from start--')
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
	print('---Print Approval obj end--')


def print_review_obj(review_obj):
	if not(review_obj):
		print('print_review_obj(): Null is being passed to print! This should not happen.')
		return
	print('---Print Review obj start--')
	print('Pk:')
	print(review_obj.pk)
	print('Bug Number:')
	print(review_obj.bug_number)
	print('Approval outcome:')
	print(review_obj.approval_outcome)
	print('Team pk:')
	print(review_obj.team.pk)
	print('Review Type:')
	print(review_obj.review_type)
	print('Num exemptions:')
	print(review_obj.num_of_exemption)
	print('---Print Review obj end--')