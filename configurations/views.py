from django.shortcuts import render,redirect
from django.http import HttpResponse,JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import LoginForm,UserRegistrationForm
from configurations.models import Team,Series,Choice,Question
from configurations.HelperClasses import ConfigurationDashboard
from django.contrib.auth.hashers import make_password
from collections import OrderedDict
from peer_review.models import Review,Approval
from peer_review.HelperClasses import CommonLookups,StatusCodes,CommonCounts,CombinedPendingReviewCount
from django.db.models.functions import ExtractMonth,ExtractYear
from django.db.models import Count
from datetime import datetime
from django.contrib.auth.decorators import login_required,user_passes_test
from configurations.HelperClasses.PermissionResolver import is_manager,is_emp_or_manager
# Create your views here.
@login_required(login_url='/reviews/login')
def index(request):	
	context={}
	context['review_raised_by_me_count']=CommonCounts.get_review_raised_by_me(request.user).count()
	context['peer_testing_raised_by_me_count']=CommonCounts.get_peer_testing_raised_by_me(request.user).count()
	context['peer_testing_raised_to_me_count']=CommonCounts.get_peer_testing_raised_to_me(request.user).count()
	context['review_raised_to_me_count']=CommonCounts.get_review_raised_to_me(request.user).count()
	context['toast_pending']=CombinedPendingReviewCount(request.user)
	return render(request,'site_pages/home_page.html',context)

@login_required(login_url='/reviews/login')
def logout_view(request):
	logout(request)
	messages.success(request, "Logged out successfully!")
	return redirect("configurations:login")

def login_view(request):
	form=LoginForm(request.POST or None)
	if request.user.is_authenticated:
		return redirect("configurations:homepage")
	if request.method=='POST':
		if form.is_valid():
			username=form.cleaned_data['username']
			password=form.cleaned_data['password']
			user = authenticate(username=username, password=password)
			if user:
				if user.is_active:
					login(request,user)
					messages.success(request,"Welcome "+username)
					return redirect("configurations:homepage")
				else:
					form.add_error('username','User '+str(user.username)+' is not active')
			else:
				form.add_error(None,'Invalid login details. Please try again')
		form.check_for_field_errors()
	return render(request, 'registration/login.html', {'form': form})

def user_registration_view(request):
	form=UserRegistrationForm(request.POST or None)
	if request.method=='POST':
		if form.is_valid():
			user_created=form.save(commit=False)
			user_created.set_password(form.cleaned_data['password'])
			form.save()
			messages.success(request,'User '+form.cleaned_data['username']+ ' created sucessfully')
			return redirect("configurations:login")
	form.check_for_field_errors()
	return render(request,'registration/userRegistration.html',{'form':form})

@login_required(login_url='/reviews/login')
@user_passes_test(is_manager,login_url='/reviews/unauthorized')
def configurations_home(request):
	team_count=Team.objects.all().count()
	series_count=Series.objects.all().count()
	choice_count=Choice.objects.all().count()
	question_count=Question.objects.all().count()
	dashboard_objects=[]
	team_obj=ConfigurationDashboard('Teams','supervisor_account',team_count,'configurations:team_list_view','image_floating_card_indigo')
	series_obj=ConfigurationDashboard('Series','timeline',series_count,'configurations:series_list_view','image_floating_card_lime')
	choice_obj=ConfigurationDashboard('Choices','check_box',choice_count,'configurations:choice_list_view','image_floating_card_brown')
	question_obj=ConfigurationDashboard('Questions','article',question_count,'configurations:question_list_view','image_floating_card_green')
	dashboard_objects.append(team_obj)
	dashboard_objects.append(series_obj)
	dashboard_objects.append(choice_obj)
	dashboard_objects.append(question_obj)
	context_dict={'dashboard_objects':dashboard_objects,'is_conf_active':'active'}
	return render(request,'configurations/configuration_home.html',context_dict)

@login_required(login_url='/reviews/login')
@user_passes_test(is_emp_or_manager,login_url='/reviews/unauthorized')
def choices_dependent_region(request):
	choice_type=request.GET.get('choice_type')
	print('Choice type ajax')
	print(choice_type)
	if choice_type=='TXT':
		return HttpResponse('Choice not needed for text type')
	choices=Choice.objects.all()
	choices_lov=OrderedDict()
	for choice in choices:
		choices_lov[choice.pk]=choice.choice_text
	return render(request,'lov/choices_dependent_region.html',{'objects':choices_lov.items()})

@login_required(login_url='/reviews/login')
@user_passes_test(is_emp_or_manager,login_url='/reviews/unauthorized')
def review_raised_graph(request):
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
	curr_year=datetime.today().year
	review_queryset=CommonCounts.get_review_raised_by_me(user=request.user,year=curr_year)\
				.annotate(month=ExtractMonth('creation_date'))\
				.values('month')\
				.annotate(count_review=Count('pk'))\
				.distinct()
	# labels.append(1)
	# labels.append(2)
	# data.append(3)
	# data.append(4)
	review_months_all=[]
	already_present_months=[]
	for item in review_queryset:
		review_months_all.append((item['month'],item['count_review']))
		already_present_months.append(item['month'])
	for i in range(1,13):
		if i not in already_present_months:
			review_months_all.append((i,0))
	review_months_all.sort()
	for i in review_months_all:
		labels.append(months_dict[i[0]])
		data.append(i[1])
	print('Review raised graph')
	print(labels,data)

	raised_to_me_review=CommonCounts.get_review_raised_to_me(user=request.user,year=curr_year)\
										.annotate(month=ExtractMonth('creation_date'))\
										.values('month')\
										.annotate(count_review=Count('pk'))\
										.distinct()
	already_present_months=[]
	raised_to_me_months_all=[]
	for item in raised_to_me_review:
		raised_to_me_months_all.append((item['month'],item['count_review']))
		already_present_months.append(item['month'])
	for i in range(1,13):
		if i not in already_present_months:
			raised_to_me_months_all.append((i,0))
	raised_to_me_months_all.sort()
	data2=[]
	for i in raised_to_me_months_all:
		data2.append(i[1])

	return JsonResponse(data={
        'labels': labels,
        'data1': data,
        'data2':data2
    })


@login_required(login_url='/reviews/login')
@user_passes_test(is_emp_or_manager,login_url='/reviews/unauthorized')
def peer_testing_graph(request):
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
	curr_year=datetime.today().year
	peer_testing_queryset=CommonCounts.get_peer_testing_raised_by_me(user=request.user,year=curr_year)\
				.annotate(month=ExtractMonth('creation_date'))\
				.values('month')\
				.annotate(count_review=Count('pk'))\
				.distinct()
	# labels.append(1)
	# labels.append(2)
	# data.append(3)
	# data.append(4)
	print(peer_testing_queryset)
	review_months_all=[]
	already_present_months=[]
	for item in peer_testing_queryset:
		review_months_all.append((item['month'],item['count_review']))
		already_present_months.append(item['month'])
	for i in range(1,13):
		if i not in already_present_months:
			review_months_all.append((i,0))
	review_months_all.sort()
	for i in review_months_all:
		labels.append(months_dict[i[0]])
		data.append(i[1])
	print('Peer testing graph')
	print(labels,data)

	raised_to_me_review=CommonCounts.get_peer_testing_raised_to_me(user=request.user,year=curr_year)\
									.annotate(month=ExtractMonth('creation_date'))\
									.values('month')\
									.annotate(count_review=Count('pk'))\
									.distinct()
	already_present_months=[]
	raised_to_me_months_all=[]
	for item in raised_to_me_review:
		raised_to_me_months_all.append((item['month'],item['count_review']))
		already_present_months.append(item['month'])
	for i in range(1,13):
		if i not in already_present_months:
			raised_to_me_months_all.append((i,0))
	raised_to_me_months_all.sort()
	data2=[]
	for i in raised_to_me_months_all:
		data2.append(i[1])

	return JsonResponse(data={
        'labels': labels,
        'data1': data,
        'data2':data2
    })

def unauthorized_message_view(request):
	return render(request,'site_pages/access_denied.html')

