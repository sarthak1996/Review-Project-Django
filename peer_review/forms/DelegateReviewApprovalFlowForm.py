from django.forms import ModelForm
from django import forms
from peer_review.models import Approval
from django.contrib.auth import get_user_model

class DelegateReviewApprovalFlowForm(ModelForm):
	raised_to=forms.ModelChoiceField(queryset=get_user_model().objects.all(),empty_label='Choose a User',widget=forms.Select(attrs={'class':'form-control choice_select'}))

	class Meta:
		model=Approval
		fields=['raised_to']

	def __init__(self, *args, **kwargs):
		request_user= kwargs.pop('request').user
		super(DelegateReviewApprovalFlowForm, self).__init__(*args, **kwargs)
		self.fields['raised_to'].queryset=get_user_model().objects.all().exclude(pk=request_user.pk).all()
		