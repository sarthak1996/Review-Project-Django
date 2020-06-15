from peer_review.HelperClasses import StatusCodes,CommonLookups,CommonCounts

class CombinedPendingReviewCount():

	def __init__(self,user):
		self.user=user

	def get_peer_testing_by_me_pending_count(self):
		return {
			'Peer testing of Sev 1 priority': CommonCounts.get_peer_testing_raised_by_me(self.user)\
				.filter(approval_outcome=StatusCodes.get_pending_status()
						,priority=CommonLookups.get_review_high_priority())\
				.count(),
			'Peer testing of Sev 2 priority': CommonCounts.get_peer_testing_raised_by_me(self.user)\
				.filter(approval_outcome=StatusCodes.get_pending_status()
						,priority=CommonLookups.get_review_normal_priority())\
				.count(),
			}.items()

	def get_peer_testing_to_me_pending_count(self):
		return {
			'Peer testing of Sev 1 priority': CommonCounts.get_peer_testing_raised_to_me(self.user)\
						.filter(approval_outcome=StatusCodes.get_pending_status(),
							review__priority=CommonLookups.get_review_high_priority())\
						.count(),
			'Peer testing of Sev 2 priority': CommonCounts.get_peer_testing_raised_to_me(self.user)\
						.filter(approval_outcome=StatusCodes.get_pending_status(),
							review__priority=CommonLookups.get_review_normal_priority())\
						.count(),
		}.items()

	def get_peer_review_by_me_pending_count(self):
		return {
			'Checklist review of Sev 1 priority': CommonCounts.get_review_raised_by_me(self.user)\
					.filter(approval_outcome=StatusCodes.get_pending_status()
							,priority=CommonLookups.get_review_high_priority())\
					.count(),
			'Checklist review of Sev 2 priority': CommonCounts.get_review_raised_by_me(self.user)\
					.filter(approval_outcome=StatusCodes.get_pending_status()
							,priority=CommonLookups.get_review_normal_priority())\
					.count(),
		}.items()

	def get_peer_review_to_me_pending_count(self):
		return {
			'Checklist review of Sev 1 priority': CommonCounts.get_review_raised_to_me(self.user)\
					.filter(approval_outcome=StatusCodes.get_pending_status(),
						review__priority=CommonLookups.get_review_high_priority())\
					.count(),
			'Checklist review of Sev 2 priority': CommonCounts.get_review_raised_to_me(self.user)\
					.filter(approval_outcome=StatusCodes.get_pending_status(),
						review__priority=CommonLookups.get_review_normal_priority())\
					.count(),
		}.items()

	def get_peer_review_to_my_team_pending_count(self):
		teams=[team for team in self.user.managed_teams.all()]
		return {
			'Checklist review of Sev 1 priority': CommonCounts.get_review_raised_by_my_team(self.user,teams)\
					.filter(approval_outcome=StatusCodes.get_pending_status(),
						priority=CommonLookups.get_review_high_priority())\
					.count(),
			'Checklist review of Sev 2 priority': CommonCounts.get_review_raised_by_my_team(self.user,teams)\
					.filter(approval_outcome=StatusCodes.get_pending_status(),
						priority=CommonLookups.get_review_normal_priority())\
					.count(),
		}.items()
	def get_peer_testing_to_my_team_pending_count(self):
		teams=[team for team in self.user.managed_teams.all()]
		return {
			'Peer testing of Sev 1 priority': CommonCounts.get_peer_testing_by_my_team(self.user,teams)\
					.filter(approval_outcome=StatusCodes.get_pending_status(),
						priority=CommonLookups.get_review_high_priority())\
					.count(),
			'Peer testing of Sev 2 priority': CommonCounts.get_peer_testing_by_my_team(self.user,teams)\
					.filter(approval_outcome=StatusCodes.get_pending_status(),
						priority=CommonLookups.get_review_normal_priority())\
					.count(),
		}.items()

	