from django.db.models.functions import ExtractYear
from peer_review.models import Approval
from peer_review.HelperClasses import CommonLookups,StatusCodes

def get_review_raised_by_me(user,year=None):
	if not year:
		return user.reviews_created_by.all()\
				.filter(review_type=CommonLookups.get_peer_review_question_type())
	return user.reviews_created_by.all()\
				.annotate(ex_year=ExtractYear('creation_date'))\
				.filter(review_type=CommonLookups.get_peer_review_question_type(),
					ex_year=year)

def get_review_raised_to_me(user,year=None):
	if not year:
		return Approval.objects.filter(latest=True,
										raised_to=user,
										review__review_type=CommonLookups.get_peer_review_question_type())
	return Approval.objects\
							.annotate(ex_year=ExtractYear('creation_date'))\
							.filter(latest=True,
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
		return Approval.objects.filter(latest=True,
										raised_to=user,
										review__review_type=CommonLookups.get_peer_testing_question_type())
	return Approval.objects\
						.annotate(ex_year=ExtractYear('creation_date'))\
						.filter(latest=True,
						raised_to=user,
						review__review_type=CommonLookups.get_peer_testing_question_type(),
						ex_year=year)


def get_perct_num_reviews_by_apr_outcome(qs,user,review_type,raised_to_me):
	total_reviews=qs.count()
	filtered_reviews=None
	if review_type==CommonLookups.get_peer_testing_question_type():
		if raised_to_me:
			filtered_reviews=get_peer_testing_raised_to_me(user)
		else:
			filtered_reviews=get_peer_testing_raised_by_me(user)
	elif review_type==CommonLookups.get_peer_review_question_type():
		if raised_to_me:
			filtered_reviews=get_review_raised_to_me(user)
		else:
			filtered_reviews=get_review_raised_by_me(user)
			print(filtered_reviews)

	num_pnd=filtered_reviews.filter(approval_outcome=StatusCodes.get_pending_status()).count()
	num_inv=filtered_reviews.filter(approval_outcome=StatusCodes.get_invalid_status()).count()
	num_rej=filtered_reviews.filter(approval_outcome=StatusCodes.get_rejected_status()).count()
	num_apr=filtered_reviews.filter(approval_outcome=StatusCodes.get_approved_status()).count()
	num_dict={'num_pnd':num_pnd,
			'num_inv':num_inv,
			'num_rej':num_rej,
			'num_apr':num_apr}

	if total_reviews!=0:
		perct_pnd=int((num_pnd/total_reviews)*100)
		perct_inv=int((num_inv/total_reviews)*100)
		perct_rej=int((num_rej/total_reviews)*100)
		perct_apr=int((num_apr/total_reviews)*100)
		perct_dict=normalize_pcts({'perct_pnd':perct_pnd,
									'perct_inv':perct_inv,
									'perct_rej':perct_rej,
									'perct_apr':perct_apr})
		
	else:
		perct_dict = {'perct_pnd':0,
			'perct_inv':0,
			'perct_rej':0,
			'perct_apr':0}
	print('Progress bar dict')
	print({**num_dict,**perct_dict})
	return {**num_dict,**perct_dict}


def normalize_pcts(perct_dict):
	# logic:
	# create clone of dict
	# remove 0 entries from cloned dict
	# find min of 0 eliminated clone
	# normalize min element to 100 - (rest sum)
	print('Perct dictionary:')
	print(perct_dict)
	zero_removed_dict={key:val for key, val in perct_dict.items() if val != 0}
	if zero_removed_dict:
		min_element=min(zero_removed_dict,key=zero_removed_dict.get)
		rest_sum=sum(zero_removed_dict.values())-zero_removed_dict.get(min_element)
		perct_dict[min_element]=100-rest_sum
	return perct_dict






