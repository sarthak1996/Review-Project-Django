from peer_review.HelperClasses import Timeline,CommonLookups

def get_approval_timeline(review,request):
	approval_rows=review.approval_review_assoc.order_by('creation_date')
	distinct_approval_objs=[approval_rows.first()]
	prev_row=approval_rows.first()

	for row in approval_rows:
		if is_approval_attribute_change(row,prev_row):
			distinct_approval_objs.append(row)
			prev_row=row

	timeline=[]
	for apr in distinct_approval_objs:
		timeline.append(Timeline(title=apr.raised_to.get_full_name(),
								description=['Approver comment: '+apr.approver_comment,'Delegated: '+str(apr.delegated)] if apr.approver_comment else None,
								is_url=False,
								request=request,
								title_right_floater=CommonLookups.get_approval_value(apr.approval_outcome))
						)
	return timeline
# assuming approval rows are passed from same review
# does not check latest attributes on the rows
def is_approval_attribute_change(apr1,apr2):
	if apr1.approval_outcome!= apr2.approval_outcome:
		return True
	if apr1.raised_to!=apr2.raised_to:
		return True
	if apr1.approver_comment!=apr2.approver_comment:
		return True
	if apr1.delegated!=apr2.delegated:
		return True
	return False
