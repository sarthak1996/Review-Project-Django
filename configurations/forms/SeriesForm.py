from django.forms import ModelForm
from configurations.models import Series
from django import forms
from concurrency.forms import VersionWidget

class SeriesForm(ModelForm):
	series_name=forms.CharField(required=True,widget=forms.TextInput(attrs={'placeholder': 'Series name','class':'form-control'}))
	series_type=forms.ChoiceField(required=False,choices=Series.get_choices_models()['series_type'],widget=forms.Select(attrs={'class':'form-control choice_select','label':'Series type'}))
	version=VersionWidget()
	class Meta:
		model=Series
		fields=['series_name','series_type','version']
