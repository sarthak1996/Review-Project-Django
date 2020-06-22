from django.forms import ModelForm
from django import forms
from django.contrib.auth import get_user_model
from peer_review.models import Review
from concurrency.forms import VersionWidget
class PeerTestingApprovalForm(ModelForm):
	approver_comment=forms.CharField(required=True,label='Comment',widget=forms.Textarea(attrs={'placeholder': 'Comment','class':'form-control text_area'}))
	version=VersionWidget(attrs={'placeholder': 'Object version number','class':'form-control version_widget',})
	class Meta:
		model=Review
		fields=['version']

	def clean_approver_comment(self):
		cleaned_data=super().clean()
		if not cleaned_data.get('approver_comment'):
			raise forms.ValidationError("Approver comment is required while approving the review.")
		return cleaned_data.get('approver_comment')