from django.forms import ModelForm
from django import forms
from peer_review.models import Exemption
from django.forms.utils import ErrorDict

class ExemptionForm(ModelForm):
	exemption_for=forms.CharField(required=True,label='Exemption for',widget=forms.TextInput(attrs={'placeholder': 'Exemption for','class':'form-control'}))
	exemption_explanation=forms.CharField(required=True,label='Exemption explanation',widget=forms.Textarea(attrs={'placeholder': 'Exemption explanation','class':'form-control text_area'}))
	
	class Meta:
		model=Exemption
		fields=['exemption_for','exemption_explanation']

	def clean_exemption_for(self):
		cleaned_data=super().clean()
		# print('In clean exemption_for')
		# print(cleaned_data)
		if 'exemption_for' in cleaned_data:
			if cleaned_data.get('exemption_for') is not None:
				return cleaned_data.get('exemption_for')

		raise forms.ValidationError("Exemption for can not be empty if exemption is to be added")

	def clean_exemption_explanation(self):
		cleaned_data=super().clean()
		# print('In clean exemption_explanation')
		# print(cleaned_data)
		if 'exemption_explanation' in cleaned_data:
			if cleaned_data.get('exemption_explanation') is not None:
				return cleaned_data.get('exemption_explanation')

		raise forms.ValidationError("Exemption explanation can not be empty if exemption is to be added")

	def full_clean(self,*args,**kwargs):
		super(ExemptionForm, self).full_clean(*args, **kwargs)
		if hasattr(self, 'cleaned_data') and self.cleaned_data.get('DELETE',False):
			self._errors = ErrorDict()


