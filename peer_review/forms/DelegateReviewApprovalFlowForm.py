from django.forms import ModelForm
from django import forms
from peer_review.models import Approval
from django.contrib.auth import get_user_model
from configurations.ModelChoiceFields import UserModelChoiceField
from configurations.models import Team
from peer_review.HelperClasses import PrintObjs
from concurrency.forms import VersionWidget
class DelegateReviewApprovalFlowForm(ModelForm):
	raised_to=UserModelChoiceField(queryset=get_user_model().objects.all(),empty_label='Choose a User',widget=forms.Select(attrs={'class':'form-control choice_select'}))
	version=VersionWidget(attrs={'placeholder': 'Object version number','class':'form-control version_widget',})
	class Meta:
		model=Approval
		fields=['raised_to','version']

	def __init__(self, *args, **kwargs):
		request_user= kwargs.pop('request').user
		team_id=kwargs.pop('team_id')
		super(DelegateReviewApprovalFlowForm, self).__init__(*args, **kwargs)
		self.fields['raised_to'].queryset=Team.objects.get(pk=team_id).user_team_assoc.all().exclude(pk=request_user.pk)
		

