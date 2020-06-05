from django import template
from peer_review.models import Review
from peer_review.FilterSets import ReviewRaisedToMeFilter,ReviewFilter

register = template.Library()


@register.simple_tag(takes_context=True)
def get_action_values(context,*args):
	if isinstance(args[0],Review):
		if len(args)==1:
			if isinstance(context['filter'],ReviewRaisedToMeFilter):
				return args[0].get_review_raised_to_me_actions()
			elif isinstance(context['filter'],ReviewFilter):
				return args[0].get_reviews_raised_by_me_actions()
		if len(args)==2:
			if args[1]=='review_approval':
				return args[0].get_review_raised_to_me_actions(exclude=['approve'])
			elif args[1]=='review_user_view':
				return args[0].get_reviews_raised_by_me_actions()
			elif args[1]==None:
				return args[0].get_actions_drop()
	else:
		return args[0].get_actions_drop()
