from django.forms import ModelForm
from django import forms
from peer_review.models import Review
from django.contrib.auth import get_user_model
from configurations.models import Team,Series
from peer_review.HelperClasses import ApprovalHelper
from configurations.ModelChoiceFields import UserModelChoiceField

class ReviewForm(ModelForm):
	bug_number=forms.CharField(required=True,widget=forms.TextInput(attrs={'placeholder': 'Bug number','class':'form-control'}))
	priority=forms.ChoiceField(required=False,choices=Review.get_review_priority_approval_types()['review_priority'],widget=forms.Select(attrs={'class':'form-control choice_select','label':'Priority'}))
	team=forms.ModelChoiceField(queryset=Team.objects.all(),empty_label='Choose a Team',widget=forms.Select(attrs={'class':'form-control choice_select'}))
	raise_to=UserModelChoiceField(queryset=get_user_model().objects.all(),empty_label='Choose a User',widget=forms.Select(attrs={'class':'form-control choice_select'}))
	# num_of_exemption=forms.IntegerField(required=False,widget=forms.TextInput(attrs={'placeholder': 'Bug number','class':'form-control'}))
	series_type=forms.ChoiceField(required=False,choices=Series.get_choices_models()['series_type'],widget=forms.Select(attrs={'class':'form-control choice_select','label':'Series Type'}))
	class Meta:
		model=Review
		fields=['bug_number','priority','team','series_type']

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
			print('Review instance exists.')
			self.initial['raise_to']=ApprovalHelper.get_latest_approval_row(review_instance).raised_to
	
			
	

	# def clean_series_type(self):
	# 	cleaned_data=super().clean()
	# 	if cleaned_data.get('series_type',False):
	# 		return cleaned_data.get('series_type')
	# 	else:
	# 		raise forms.ValidationError("Series type field can not be empty")
	# def clean_raised_to(self):
	# 	clean_data=super().clean()
	# 	review=self.instance.review
	# 	print('Review : ')
	# 	PrintObjs.print_review_obj(review)
	# 	team_from_raised_to=get_user_model().get(pk=clean_data.get('raised_to')).team.pk
	# 	print('Team from raised to:')
	# 	print(team_from_raised_to)
	# 	if team_from_raised_to != review.team.pk:
	# 		raise forms.ValidationError('User does not belong to the team for which the review was raised')
	# 	return clean_data.get('raised_to')

