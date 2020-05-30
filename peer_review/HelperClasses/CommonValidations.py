'''
Pass user instance and team instance
'''
def user_exists_in_team(user,team):
	return team.user_team_assoc.all().filter(pk=user.pk).exists()