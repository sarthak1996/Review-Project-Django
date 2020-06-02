import django_filters
from peer_review.models import Review
from django import forms
from django.db.models import Q

class ReviewFilter(django_filters.FilterSet):
	raised_to=django_filters.CharFilter(field_name='approval_review_assoc__raised_to',widget=forms.TextInput(attrs={'placeholder':'Raised to contains','class': 'filter_hidden'}),method='filter_by_raised_to')
	class Meta:
		model=Review
		fields={'bug_number':['icontains'],
		'priority':['exact'],
		'approval_outcome':['exact'],
		'team':['exact'],
		'series_type':['exact']}

	def filter_by_raised_to(self,queryset,name,value):
		return queryset.filter(Q(approval_review_assoc__raised_to__first_name__contains=value)
								|Q(approval_review_assoc__raised_to__last_name__contains=value),approval_review_assoc__latest=True)