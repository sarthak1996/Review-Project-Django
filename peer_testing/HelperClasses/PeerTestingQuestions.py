from peer_review.HelperClasses import CommonLookups
from configurations.models import Question
from peer_testing.models import Answer
from configurations.HelperClasses import LoggingHelper
import traceback
def get_answer_form_sets_for_peer_testing(request):
	peer_testing_type=CommonLookups.get_peer_testing_question_type()
	questions=Question.objects.filter(question_type=peer_testing_type)
	initial_questions=[]
	for question in questions:
		initial_questions.append({'question':question})
	logger=LoggingHelper(request.user,__name__)
	logger.write(str(initial_questions),LoggingHelper.DEBUG)
	return initial_questions
	
#assuming that complete review object/answer object is present
def construct_init_dictionary(review,request):
	answers=Answer.objects.filter(review=review)
	initial_answers=[]
	for answer in answers:
		answer_key='single_choice_field' if answer.question.question_choice_type==CommonLookups.get_single_choice_question_type() else 'text_answer'
		initial_answers.append({
			answer_key:answer.answer,
			'question':answer.question
			})
	logger=LoggingHelper(request.user,__name__)
	logger.write(str(initial_answers),LoggingHelper.DEBUG)
	return initial_answers