import django_filters
from configurations.models import Team
from django import forms

class TeamFilter(django_filters.FilterSet):
	# Team_text__icontains=django_filters.CharFilter(widget=forms.TextInput(attrs={'placeholder': 'Team text contains'}))
	class Meta:
		model=Team
		fields={'team_name':['icontains'],
		'team_grp_mail':['icontains']}