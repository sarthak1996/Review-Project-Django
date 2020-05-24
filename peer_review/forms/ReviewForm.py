from django.forms import ModelForm
from django import forms
from peer_review.models import Review
from django.contrib.auth import get_user_model
from configurations.models import Team

class ReviewForm(ModelForm):
	bug_number=forms.CharField(required=True,widget=forms.TextInput(attrs={'placeholder': 'Bug number','class':'form-control'}))
	priority=forms.ChoiceField(required=False,choices=Review.get_review_priority_approval_types()['review_priority'],widget=forms.Select(attrs={'class':'form-control choice_select','label':'Priority'}))
	team=forms.ModelChoiceField(queryset=Team.objects.all(),empty_label='Choose a Team',widget=forms.Select(attrs={'class':'form-control choice_select'}))
	raise_to=forms.ModelChoiceField(queryset=get_user_model().objects.all(),empty_label='Choose a User',widget=forms.Select(attrs={'class':'form-control choice_select'}))
	class Meta:
		model=Review
		fields=['bug_number','priority','team']

	def __init__(self, *args, **kwargs):
		request_user= kwargs.pop('request').user
		super(ReviewForm, self).__init__(*args, **kwargs)
		self.fields['raise_to'].queryset=get_user_model().objects.all().exclude(pk=request_user.pk).all()
		