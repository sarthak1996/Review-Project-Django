from configurations.models import Question
from peer_review.HelperClasses import CommonLookups
def get_answer_form_sets_for_peer_review():
	peer_review_type=CommonLookups.get_peer_review_question_type()
	questions=Question.objects.filter(question_type=peer_review_type)
	initial_questions=[]
	for question in questions:
		initial_questions.append({'question':question})
	print(initial_questions)
	return initial_questions