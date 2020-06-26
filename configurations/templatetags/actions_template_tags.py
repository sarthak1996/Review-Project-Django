from django import template
from peer_review.models import Review
from peer_review.FilterSets import ReviewRaisedToMeFilter,ReviewFilter
from peer_review.HelperClasses import ApprovalHelper
from configurations.HelperClasses import LoggingHelper
import traceback
register = template.Library()


# args[0] - object instance
# args[1] - type of review
# args[2] - True or False (to exclude or include Approve in actions (on listview and detailview))
# args[3] - flag to check if logged in user = request user. (get from context)
@register.simple_tag(takes_context=True)
def get_action_values(context,*args):
	logger=LoggingHelper(context['logged_in_user'],__name__)
	logger.write('Actions',LoggingHelper.DEBUG)
	logger.write('args:'+str(args),LoggingHelper.DEBUG)

	if isinstance(args[0],Review):
		# if len(args)>=4: #only check for review objects (configuration objects are already secured via manager perm and not via individual created objects)
		# 	if args[3] : #to check if logged in user = created by
		# 		if context['logged_in_user']!=context['created_by_user']:
		# 			return None
		exclude=['approve']
		if len(args)>=3:
			if args[2]:
				exclude=None
		if args[1]=='review_approval':
			if context['logged_in_user']!=context['raised_to_user']:
						return None
			return args[0].get_review_raised_to_me_actions(exclude=exclude)
		elif args[1]=='testing_review_approval':
			if context['logged_in_user']!=context['raised_to_user']:
						return None
			return args[0].get_peer_testing_raised_to_me_actions()
		elif args[1]=='review_user_view':
			if context['logged_in_user']!=context['created_by_user']:
						return None
			return args[0].get_reviews_raised_by_me_actions()
		elif args[1]=='testing_review_user_view':
			if context['logged_in_user']!=context['created_by_user']:
						return None
			return args[0].get_peer_testing_raised_by_me_actions()
		elif args[1]=='review_list_view':
			if context['logged_in_user']!=args[0].created_by:
						return None
			return args[0].get_reviews_raised_by_me_actions()
		elif args[1]=='review_to_me_list_view':
			latest_apr_row=ApprovalHelper.get_latest_approval_row(args[0],context['logged_in_user'])
			if context['logged_in_user']!=latest_apr_row.raised_to:
						return None
			return args[0].get_review_raised_to_me_actions()
		elif args[1]=='peer_testing_list_view':
			if context['logged_in_user']!=args[0].created_by:
						return None
			return args[0].get_peer_testing_raised_by_me_actions()
		elif args[1]=='peer_testing_to_me_list_view':
			latest_apr_row=ApprovalHelper.get_latest_approval_row(args[0],context['logged_in_user'])
			if context['logged_in_user']!=latest_apr_row.raised_to:
						return None
			return args[0].get_peer_testing_raised_to_me_actions()
		elif args[1]=='manager_view':
			return args[0].get_follow_up_action_manager()
	else:
		return args[0].get_actions_drop()
