from django import forms
from django.conf import settings
from django.contrib.auth import get_user_model
from configurations.models import Team


class UserRegistrationForm(forms.ModelForm):
	confirm_password=forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password','class':'form-control'}))
	password=forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password','class':'form-control'}))
	first_name=forms.CharField(required=True,widget=forms.TextInput(attrs={'placeholder': 'First name','class':'form-control'}))
	last_name=forms.CharField(required=True,widget=forms.TextInput(attrs={'placeholder': 'Last name','class':'form-control'}))
	username=forms.CharField(required=True,widget=forms.TextInput(attrs={'placeholder': 'Username','class':'form-control'}))
	email=forms.EmailField(required=True,widget=forms.EmailInput(attrs={'placeholder': 'Email','class':'form-control'}))
	team=forms.ModelChoiceField(queryset=Team.objects.all(),empty_label='Choose a Team',widget=forms.Select(attrs={'class':'form-control'}))
	field_order=['first_name','last_name','username','email','team','password','confirm_password']
	class Meta:
		model=get_user_model()
		fields =['username','password','email','team','first_name','last_name']

	def clean_confirm_password(self):
		cleaned_data=super().clean()
		if cleaned_data.get('confirm_password')==cleaned_data.get('password'):
			return cleaned_data.get('confirm_password')
		else:
			raise forms.ValidationError("Passwords do not match! Enter again")
	def clean_team(self):
		cleaned_data=super().clean()
		if cleaned_data.get('team') is not None:
			return cleaned_data.get('team')
		else:
			raise forms.ValidationError("Team field can not be empty")
	def clean_email(self):
		cleaned_data=super().clean()
		input_email=cleaned_data.get('email')
		user_with_email=get_user_model().objects.filter(email=input_email)
		if user_with_email.exists():
			raise forms.ValidationError("Email is already registered! Contact admin")
		else:
			return input_email
	def check_for_field_errors(self):
		for field in self.fields:
			if field in self.errors:
				classes=self.fields[field].widget.attrs.get("class")
				classes+=" error_field "
				self.fields[field].widget.attrs["class"]=classes

