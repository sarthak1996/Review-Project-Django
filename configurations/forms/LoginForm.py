from django import forms


class LoginForm(forms.Form):
    username = forms.CharField(label='Username', max_length=100,widget=forms.TextInput(attrs={'placeholder': 'Username','class':'form-control','autofocus': 'autofocus'}))
    password=forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password','class':'form-control'}))
    field_order=['username','password']

    def check_for_field_errors(self):
    	for field in self.fields:
    		if field in self.errors:
    			classes=self.fields[field].widget.attrs.get("class")
    			classes+=" error_field "
    			self.fields[field].widget.attrs["class"]=classes
