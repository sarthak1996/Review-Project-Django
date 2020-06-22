from django import forms

class SetPasswordForm(forms.Form):
	password=forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password','class':'form-control'}))
	confirm_password=forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password','class':'form-control'}))
	

	def clean_confirm_password(self):
		cleaned_data=super().clean()
		# print('Inside clean_confirm_password')
		# print(cleaned_data)
		if cleaned_data.get('confirm_password')==cleaned_data.get('password'):
			return cleaned_data.get('confirm_password')
		else:
			raise forms.ValidationError("Passwords do not match! Enter again")