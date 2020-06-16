from django.shortcuts import render
from peer_review.HelperClasses import CommonCounts,CombinedPendingReviewCount
from manager_activities.HelperClasses import ManagerDashboardCount
from django.contrib.auth.decorators import user_passes_test,login_required
from configurations.HelperClasses.PermissionResolver import is_manager
from datetime import datetime
from django.db.models.functions import ExtractMonth,ExtractYear
from django.db.models import Count
from django.http import HttpResponse,JsonResponse
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

@login_required(login_url='/reviews/login')
@user_passes_test(is_manager,login_url='/reviews/unauthorized')
def peer_testing_graph_manager(request):
	curr_year=datetime.today().year
	teams=[team for team in request.user.managed_teams.all()]
	qs=CommonCounts.get_peer_testing_by_my_team(user=request.user,year=curr_year,teams=teams)\
				.annotate(month=ExtractMonth('creation_date'))\
				.values('month','team')\
				.annotate(count_review=Count('pk'))\
				.distinct()
	return graph_manager(request,qs,teams)


@login_required(login_url='/reviews/login')
@user_passes_test(is_manager,login_url='/reviews/unauthorized')
def peer_review_graph_manager(request):
	curr_year=datetime.today().year
	teams=[team for team in request.user.managed_teams.all()]
	qs=CommonCounts.get_review_raised_by_my_team(user=request.user,year=curr_year,teams=teams)\
				.annotate(month=ExtractMonth('creation_date'))\
				.values('month','team')\
				.annotate(count_review=Count('pk'))\
				.distinct()
	return graph_manager(request,qs,teams)
	


@login_required(login_url='/reviews/login')
@user_passes_test(is_manager,login_url='/reviews/unauthorized')
def graph_manager(request,qs,teams):
	labels=[]
	data=[]
	months_dict={
		1:'Jan',
		2:'Feb',
		3:'Mar',
		4:'Apr',
		5:'May',
		6:'Jun',
		7:'Jul',
		8:'Aug',
		9:'Sep',
		10:'Oct',
		11:'Nov',
		12:'Dec'
	}
	
	generic_queryset=qs

	bg_colors=['rgba(255,61,0,0.3)',
				'rgba(170,0,255,0.3)',
				'rgba(100,255,218, 0.3)',
				'rgba(118,255,3, 0.3)']
				
	border_colors=['rgba(255,61,0,0.8)',
				'rgba(170,0,255,0.8)',
				'rgba(100,255,218, 0.8)',
				'rgba(118,255,3, 0.8)']
	dataset=[]
	for idx,team in enumerate(teams):
		# print('Hi '+ str(team))
		team_qs=generic_queryset.filter(team=team)
		months_all=[]
		already_present_months=[]
		data=[]
		labels=[]
		for item in team_qs:
			months_all.append((item['month'],item['count_review']))
			already_present_months.append(item['month'])
		for i in range(1,13):
			if i not in already_present_months:
				months_all.append((i,0))
		months_all.sort()
		for i in months_all:
			labels.append(months_dict[i[0]])
			data.append(i[1])
		
		dataset.append({
			'label' :str(team),
			'backgroundColor' : bg_colors[idx%len(bg_colors)],
			'borderColor' : border_colors[idx%len(border_colors)],
			'data' :data
		})
	# labels.append(1)
	# labels.append(2)
	# data.append(3)
	# data.append(4)
	# print(peer_testing_queryset)

	return JsonResponse(data={
        'labels': labels,
        'dataset': dataset
    })