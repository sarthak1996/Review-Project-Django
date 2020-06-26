from django.forms import ModelForm
from django import forms
from peer_review.models import Review
from django.contrib.auth import get_user_model
from configurations.models import Team,Series
from peer_review.HelperClasses import ApprovalHelper,CommonLookups
from configurations.ModelChoiceFields import UserModelChoiceField
from concurrency.forms import VersionWidget

class ReviewForm(ModelForm):
	bug_number=forms.CharField(required=True,widget=forms.TextInput(attrs={'placeholder': 'Bug number','class':'form-control'}))
	priority=forms.ChoiceField(required=False,initial=CommonLookups.get_review_normal_priority(),choices=Review.get_review_priority_approval_types()['review_priority'],widget=forms.Select(attrs={'class':'form-control choice_select','label':'Priority'}))
	team=forms.ModelChoiceField(queryset=Team.objects.all(),empty_label='Choose a Team',widget=forms.Select(attrs={'class':'form-control choice_select'}))
	raise_to=UserModelChoiceField(queryset=get_user_model().objects.all(),empty_label='Choose a User',widget=forms.Select(attrs={'class':'form-control choice_select'}))
	# num_of_exemption=forms.IntegerField(required=False,widget=forms.TextInput(attrs={'placeholder': 'Bug number','class':'form-control'}))
	series_type=forms.ChoiceField(required=False,choices=Series.get_choices_models()['series_type'],widget=forms.Select(attrs={'class':'form-control choice_select','label':'Series Type'}))
	version=VersionWidget(attrs={'placeholder': 'Object version number','class':'form-control version_widget',})
	class Meta:
		model=Review
		fields=['bug_number','priority','team','series_type','version']

	def __init__(self, *args, **kwargs):
		request_user= kwargs.pop('request').user
		super(ReviewForm, self).__init__(*args, **kwargs)
		review_instance=self.instance
		# self.fields['raise_to'].queryset=get_user_model().objects.none()
		if 'team' in self.initial:
			team_id=self.initial['team']
			user_team_obj=Team.objects.get(pk=team_id).user_team_assoc.all().exclude(pk=request_user.pk).all()
			self.fields['raise_to'].queryset=user_team_obj
		else: 
			self.fields['raise_to'].queryset=get_user_model().objects.all()
		if review_instance and review_instance.pk:
			self.initial['raise_to']=ApprovalHelper.get_latest_approval_row(review_instance,request_user).raised_to
	
			
