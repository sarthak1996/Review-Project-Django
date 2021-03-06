from django.forms import ModelForm
from django import forms
from django.contrib.auth import get_user_model
from peer_review.models import Review
from concurrency.forms import VersionWidget
class FollowUpForm(ModelForm):
	approver_comment=forms.CharField(required=False,label='Follow up comment',widget=forms.Textarea(attrs={'placeholder': 'If left empty then "Gentle Reminder" would be sent in email','class':'form-control text_area'}))
	version=VersionWidget(attrs={'placeholder': 'Object version number','class':'form-control version_widget',})
	class Meta:
		model=Review
		fields=['version']

	def clean_approver_comment(self):
		cleaned_data=super().clean()
		if not cleaned_data.get('approver_comment'):
			return 'Gentle reminder'
		return cleaned_data.get('approver_comment')