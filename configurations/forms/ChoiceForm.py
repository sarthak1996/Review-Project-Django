from django.forms import ModelForm
from configurations.models import Choice
from django import forms

class ChoiceForm(ModelForm):
	choice_text=forms.CharField(required=True,widget=forms.TextInput(attrs={'placeholder': 'Choice Text','class':'form-control'}))
	class Meta:
		model=Choice
		fields=['choice_text']