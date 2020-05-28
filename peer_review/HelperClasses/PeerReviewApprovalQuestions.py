from configurations.models import Question,Series
from peer_review.HelperClasses import CommonLookups
def get_answer_form_sets_for_peer_review(review):
	peer_review_type=CommonLookups.get_peer_review_question_type()
	questions=Question.objects.filter(question_type=peer_review_type,series_type=Series.get_choices_models()['series_type'][1][0])
	initial_questions=[]
	for question in questions:
		initial_questions.append({'question':question})
	if review.series_type==Series.get_choices_models()['series_type'][0][0]:
		aru_questions=Question.objects.filter(question_type=peer_review_type,series_type=review.series_type)
		for question in aru_questions:
			initial_questions.append({'question':question})
	print(initial_questions)
	return initial_questions