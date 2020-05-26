from django.forms import ModelForm
from django import forms
from peer_review.models import Exemption

class ExemptionForm(ModelForm):
	exemption_for=forms.CharField(required=False,label='Exemption for',widget=forms.TextInput(attrs={'placeholder': 'Exemption for','class':'form-control not_rendered'}))
	exemption_explanation=forms.CharField(required=False,label='Exemption explanation',widget=forms.TextInput(attrs={'placeholder': 'Exemption explanation','class':'form-control not_rendered'}))
	
	class Meta:
		model=Exemption
		fields=['exemption_for','exemption_explanation']

