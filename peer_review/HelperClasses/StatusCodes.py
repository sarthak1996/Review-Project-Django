from peer_review.HelperClasses import CommonLookups

APPROVAL_OUTCOMES=CommonLookups.get_approval_outcomes()

def get_approved_status():
	return APPROVAL_OUTCOMES[0][0]

def get_pending_status():
	return APPROVAL_OUTCOMES[1][0]

def get_rejected_status():
	return APPROVAL_OUTCOMES[2][0]

def get_invalid_status():
	return APPROVAL_OUTCOMES[3][0]