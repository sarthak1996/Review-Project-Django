from django.forms import ModelForm
from django import forms
from django.contrib.auth import get_user_model
from configurations.ModelChoiceFields import UserModelChoiceField
from peer_review.models import Review
from peer_review.HelperClasses import ApprovalHelper
from configurations.models import Team
class PeerTestingReviewForm(ModelForm):
	bug_number=forms.CharField(required=True,widget=forms.TextInput(attrs={'placeholder': 'Bug number','class':'form-control'}))
	priority=forms.ChoiceField(required=False,choices=Review.get_review_priority_approval_types()['review_priority'],widget=forms.Select(attrs={'class':'form-control choice_select','label':'Priority'}))
	team=forms.ModelChoiceField(queryset=Team.objects.all(),empty_label='Choose a Team',widget=forms.Select(attrs={'class':'form-control choice_select'}))
	raise_to=UserModelChoiceField(queryset=get_user_model().objects.all(),empty_label='Choose a User',widget=forms.Select(attrs={'class':'form-control choice_select'}))
	class Meta:
		model=Review
		fields=['bug_number','priority','team']

	def __init__(self, *args, **kwargs):
		request_user= kwargs.pop('request').user
		super(PeerTestingReviewForm, self).__init__(*args, **kwargs)
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
	