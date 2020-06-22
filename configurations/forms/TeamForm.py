from django.forms import ModelForm
from configurations.models import Team
from django import forms
from concurrency.forms import VersionWidget

class TeamForm(ModelForm):
	team_name=forms.CharField(required=True,widget=forms.TextInput(attrs={'placeholder': 'Team Name','class':'form-control'}))
	team_grp_mail=forms.EmailField(required=True,widget=forms.EmailInput(attrs={'placeholder': 'Team Group Email','class':'form-control'}))
	version=VersionWidget(attrs={'placeholder': 'Object version number','class':'form-control version_widget',})
	class Meta:
		model=Team
		fields=['team_name','team_grp_mail','version']