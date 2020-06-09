import django_filters
from peer_review.models import Review
from django import forms
from django.db.models import Q

class ReviewRaisedToMeFilter(django_filters.FilterSet):
	raised_by=django_filters.CharFilter(field_name='created_by',widget=forms.TextInput(attrs={'placeholder':'Raised to contains','class': 'filter_hidden'}),method='filter_by_raised_by')
	class Meta:
		model=Review
		fields={'bug_number':['icontains'],
		'priority':['exact'],
		'approval_outcome':['exact'],
		'series_type':['exact']}

	def filter_by_raised_by(self,queryset,name,value):
		return queryset.filter(Q(created_by__first_name__contains=value)
								|Q(created_by__last_name__contains=value))