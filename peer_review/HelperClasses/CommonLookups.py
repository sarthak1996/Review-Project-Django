
REVIEW_PRIORITY=[(1,"High Priority (Sev1)"),(2,"Normal priority (Sev2)")]
APPROVAL_OUTCOMES=[('APR','APPROVED'),('PND','PENDING'),('REJ','REJECTED'),('INV','INVALID')]
QUESTION_CHOICE_TYPE=[("SCH","Single choice"),("MCH","Multiple choice"),("TXT","Text")]
QUESTION_TYPE=[("PRTEST","Peer Testing"),("MRGCHK","Mergereq checklist")]
SERIES_TYPE=[("ARU","ARU"),("","Non-ARU")]

def get_peer_review_question_type():
	return get_question_types()[1][0]

def get_peer_testing_question_type():
	return get_question_types()[0][0]

def get_single_choice_question_type():
	return get_question_choice_types()[0][0]

def get_multi_choice_question_type():
	return get_question_choice_types()[1][0]

def get_text_question_type():
	return get_question_choice_types()[2][0]

def get_review_priorities():
	return REVIEW_PRIORITY

def get_review_high_priority():
	return REVIEW_PRIORITY[0][0]

def get_review_normal_priority():
	return REVIEW_PRIORITY[1][0]

def get_approval_outcomes():
	return APPROVAL_OUTCOMES

def get_question_choice_types():
	return QUESTION_CHOICE_TYPE

def get_question_types():
	return QUESTION_TYPE

def get_series_types():
	return SERIES_TYPE

def get_aru_series_type():
	return SERIES_TYPE[0][0]

def get_aru_series_type_name():
	return SERIES_TYPE[0][1]

def get_non_aru_series_type():
	return SERIES_TYPE[1][0]

def get_non_aru_series_type_name():
	return SERIES_TYPE[1][1]

def get_approval_value(status_code):
	return ''.join([value for (item,value) in APPROVAL_OUTCOMES if item==status_code])
	
