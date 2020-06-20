from django import forms

class PasswordResetRequestForm(forms.Form):
    email_or_username = forms.CharField(label=("Email Or Username"), max_length=254,widget=forms.TextInput(attrs={'placeholder': 'Email','class':'form-control'}))