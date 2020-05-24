from django.forms import ModelForm
from configurations.models import Team
from django import forms

class TeamForm(ModelForm):
	team_name=forms.CharField(required=True,widget=forms.TextInput(attrs={'placeholder': 'Team Name','class':'form-control'}))
	team_grp_mail=forms.EmailField(required=True,widget=forms.EmailInput(attrs={'placeholder': 'Team Group Email','class':'form-control'}))
	class Meta:
		model=Team
		fields=['team_name','team_grp_mail']