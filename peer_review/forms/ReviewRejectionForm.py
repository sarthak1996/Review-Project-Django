from django.forms import ModelForm
from django import forms
from django.contrib.auth import get_user_model
from peer_review.models import Review
class ReviewRejectionForm(ModelForm):
	approver_comment=forms.CharField(required=True,label='Comment',widget=forms.TextInput(attrs={'placeholder': 'Comment','class':'form-control'}))
	class Meta:
		model=Review
		fields=[]

	def clean_approver_comment(self):
		cleaned_data=super().clean()
		if not cleaned_data.get('approver_comment'):
			raise forms.ValidationError("Approver comment is required while rejecting the review.")
		return cleaned_data.get('approver_comment')
