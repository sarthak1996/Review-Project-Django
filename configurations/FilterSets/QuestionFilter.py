import django_filters
from configurations.models import Question
from django import forms

class QuestionFilter(django_filters.FilterSet):
	# question_text__icontains=django_filters.CharFilter(widget=forms.TextInput(attrs={'placeholder': 'Question text contains'}))
	class Meta:
		model=Question
		fields={'question_text':['icontains'],
		'question_choice_type':['exact'],
		'mandatory':['exact'],
		'series_type':['exact'],
		'question_type':['exact']}
