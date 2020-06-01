import django_filters
from configurations.models import Series
from django import forms

class SeriesFilter(django_filters.FilterSet):
	# Series_text__icontains=django_filters.CharFilter(widget=forms.TextInput(attrs={'placeholder': 'Series text contains'}))
	class Meta:
		model=Series
		fields={'series_name':['icontains'],
				'series_type':['exact']}