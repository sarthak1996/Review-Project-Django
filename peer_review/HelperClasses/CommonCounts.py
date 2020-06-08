from django.db.models.functions import ExtractYear
from peer_review.models import Approval
from peer_review.HelperClasses import CommonLookups

def get_review_raised_by_me(user,year=None):
	if not year:
		user.reviews_created_by.all()\
				.filter(review_type=CommonLookups.get_peer_review_question_type())
	return user.reviews_created_by.all()\
				.annotate(ex_year=ExtractYear('creation_date'))\
				.filter(review_type=CommonLookups.get_peer_review_question_type(),
					ex_year=year)

def get_review_raised_to_me(user,year=None):
	if not year:
		return Approval.objects.filter(latest='True',
										raised_to=user,
										review__review_type=CommonLookups.get_peer_review_question_type())
	return Approval.objects\
							.annotate(ex_year=ExtractYear('creation_date'))\
							.filter(latest='True',
									raised_to=user,
									review__review_type=CommonLookups.get_peer_review_question_type(),
									ex_year=year)

def get_peer_testing_raised_by_me(user,year=None):
	if not year:
		return user.reviews_created_by.all().\
				filter(review_type=CommonLookups.get_peer_testing_question_type())
	return user.reviews_created_by.all()\
							.annotate(ex_year=ExtractYear('creation_date'))\
							.filter(review_type=CommonLookups.get_peer_testing_question_type(),
												ex_year=year)

def get_peer_testing_raised_to_me(user,year=None):
	if not year:
		return Approval.objects.filter(latest='True',
										raised_to=user,
										review__review_type=CommonLookups.get_peer_testing_question_type())
	return Approval.objects\
						.annotate(ex_year=ExtractYear('creation_date'))\
						.filter(latest='True',
						raised_to=user,
						review__review_type=CommonLookups.get_peer_testing_question_type(),
						ex_year=year)
