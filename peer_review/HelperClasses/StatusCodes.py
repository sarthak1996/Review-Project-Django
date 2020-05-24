from peer_review.models import Review
APPROVAL_OUTCOMES=Review.get_review_priority_approval_types()['approval_outcome']

def get_approved_status():
	return APPROVAL_OUTCOMES[0][0]

def get_pending_status():
	return APPROVAL_OUTCOMES[1][0]

def get_rejected_status():
	return APPROVAL_OUTCOMES[2][0]

def get_invalid_status():
	return APPROVAL_OUTCOMES[3][0]