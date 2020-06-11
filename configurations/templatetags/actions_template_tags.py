from django import template
from peer_review.models import Review
from peer_review.FilterSets import ReviewRaisedToMeFilter,ReviewFilter

register = template.Library()


@register.simple_tag(takes_context=True)
def get_action_values(context,*args):
	print('Actions')
	print(args)
	if isinstance(args[0],Review):
		exclude=['approve']
		if len(args)==3:
			if args[2]:
				exclude=None
		if args[1]=='review_approval':
			return args[0].get_review_raised_to_me_actions(exclude=exclude)
		elif args[1]=='testing_review_approval':
			return args[0].get_peer_testing_raised_to_me_actions(exclude=exclude)
		elif args[1]=='review_user_view':
			return args[0].get_reviews_raised_by_me_actions()
		elif args[1]=='testing_review_user_view':
			return args[0].get_peer_testing_raised_by_me_actions()
	else:
		return args[0].get_actions_drop()
