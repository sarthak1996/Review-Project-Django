from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import LoginForm,UserRegistrationForm
from configurations.models import Team,Series,Choice,Question
from configurations.HelperClasses import ConfigurationDashboard
from django.contrib.auth.hashers import make_password

# Create your views here.
def index(request):
	if request.user.is_authenticated:
		return render(request,'site_pages/home_page.html')
	else:
		return redirect("configurations:login")

def logout_view(request):
	logout(request)
	messages.info(request, "Logged out successfully!")
	return redirect("configurations:homepage")

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
			return redirect("configurations:login")
	form.check_for_field_errors()
	return render(request,'registration/userRegistration.html',{'form':form})

def configurations_home(request):
	team_count=Team.objects.all().count()
	series_count=Series.objects.all().count()
	choice_count=Choice.objects.all().count()
	question_count=Question.objects.all().count()
	dashboard_objects=[]
	team_obj=ConfigurationDashboard('Teams','',team_count,'configurations:team_list_view')
	series_obj=ConfigurationDashboard('Series','',series_count,'configurations:series_list_view')
	choice_obj=ConfigurationDashboard('Choices','',choice_count,'configurations:choice_list_view')
	question_obj=ConfigurationDashboard('Questions','',question_count,'configurations:question_list_view')
	dashboard_objects.append(team_obj)
	dashboard_objects.append(series_obj)
	dashboard_objects.append(choice_obj)
	dashboard_objects.append(question_obj)
	context_dict={'dashboard_objects':dashboard_objects}
	return render(request,'configurations/configuration_home.html',context_dict)
