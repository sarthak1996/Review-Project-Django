from configurations.models import Question
def get_peer_review_question_type():
	return Question.get_questions_choice_types()['question_type'][1][0]

def get_peer_testing_question_type():
	return Question.get_questions_choice_types()['question_type'][0][0]

def get_single_choice_question_type():
	return Question.get_questions_choice_types()['question_choice_type'][0][0]

def get_multi_choice_question_type():
	return Question.get_questions_choice_types()['question_choice_type'][1][0]

def get_text_question_type():
	return Question.get_questions_choice_types()['question_choice_type'][2][0]
	
