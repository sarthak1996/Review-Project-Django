from configurations.models import Question,Series
from peer_review.HelperClasses import CommonLookups
from configurations.HelperClasses import LoggingHelper
import traceback
def get_answer_form_sets_for_peer_review(review,request):
	logger=LoggingHelper(request.user,__name__)
	peer_review_type=CommonLookups.get_peer_review_question_type()
	questions=Question.objects.filter(question_type=peer_review_type,series_type=CommonLookups.get_non_aru_series_type())
	initial_questions=[]
	for question in questions:
		initial_questions.append({'question':question}) 
	if review.series_type==CommonLookups.get_aru_series_type():
		aru_questions=Question.objects.filter(question_type=peer_review_type,series_type=review.series_type)
		for question in aru_questions:
			initial_questions.append({'question':question})
	logger.write(str(initial_questions),LoggingHelper.DEBUG)
	return initial_questions