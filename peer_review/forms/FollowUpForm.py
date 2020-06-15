from django.forms import ModelForm
from django import forms
from django.contrib.auth import get_user_model
from peer_review.models import Review
class FollowUpForm(ModelForm):
	approver_comment=forms.CharField(required=False,label='Follow up comment',widget=forms.Textarea(attrs={'placeholder': 'If left empty then "Gentle Reminder" would be sent in email','class':'form-control text_area'}))
	class Meta:
		model=Review
		fields=[]

	def clean_approver_comment(self):
		cleaned_data=super().clean()
		# print('Followup form')
		# print(cleaned_data)
		# print(not cleaned_data.get('approver_comment'))
		if not cleaned_data.get('approver_comment'):
			return 'Gentle reminder'
		return cleaned_data.get('approver_comment')