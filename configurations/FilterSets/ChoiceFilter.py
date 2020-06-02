import django_filters
from configurations.models import Choice
from django import forms

class ChoiceFilter(django_filters.FilterSet):
	# question_text__icontains=django_filters.CharFilter(widget=forms.TextInput(attrs={'placeholder': 'Question text contains'}))
	class Meta:
		model=Choice
		fields={'choice_text':['icontains']}