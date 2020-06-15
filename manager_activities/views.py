from django.shortcuts import render
from peer_review.HelperClasses import CommonCounts,CombinedPendingReviewCount
from manager_activities.HelperClasses import ManagerDashboardCount
from django.contrib.auth.decorators import user_passes_test,login_required
from configurations.HelperClasses.PermissionResolver import is_manager
# Create your views here.

@login_required(login_url='/reviews/login')
@user_passes_test(is_manager,login_url='/reviews/unauthorized')
def manager_view_landing_page(request):
	context={}
	teams=[team for team in request.user.managed_teams.all()]
	colors=['image_floating_card_red','image_floating_card_green','image_floating_card_indigo','image_floating_card_lime','image_floating_card_brown']
	manager_counts=[]
	for idx,team in enumerate(teams):
		count=CommonCounts.get_review_raised_by_my_team(request.user,[team]).count()
		title='Peer Reviews'
		url='manager_activities:peer_review_manager_list'
		filter='?filter_form-approval_outcome=PND&filter_form-team='+team.team_name#add team and pending filter
		manager_counts.append(ManagerDashboardCount(title=title,
													team=team.team_name,
													count=count,
													filter=filter,
													icon='article',
													color=colors[idx%len(colors)],
													url=url
													))
		count=CommonCounts.get_peer_testing_by_my_team(request.user,[team]).count()
		title='Peer Testings'
		url='manager_activities:peer_testing_manager_list'
		filter='?filter_form-approval_outcome=PND&filter_form-team='+team.team_name#add team and pending filter
		manager_counts.append(ManagerDashboardCount(title=title,
													team=team.team_name,
													count=count,
													filter=filter,
													icon='assignment',
													color=colors[(idx+1)%len(colors)],
													url=url
													))

	context['manager_counts']=manager_counts
	context['is_man_home_active']='active'
	context['toast_pending']=CombinedPendingReviewCount(request.user)
	return render(request,'manager_activities/manager_home.html',context)