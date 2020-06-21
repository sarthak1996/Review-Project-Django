from django.forms import ModelForm
from configurations.models import Choice
from django import forms
from concurrency.forms import VersionWidget

class ChoiceForm(ModelForm):
	choice_text=forms.CharField(required=True,widget=forms.TextInput(attrs={'placeholder': 'Choice Text','class':'form-control'}))
	version=VersionWidget()
	class Meta:
		model=Choice
		fields=['choice_text','version']