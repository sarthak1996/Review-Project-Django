from django.views.generic import FormView
from configurations.forms import SetPasswordForm
from django.contrib.auth import get_user_model
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.contrib import messages
from django.shortcuts import render,redirect
class PasswordResetConfirmView(FormView):
    template_name = "registration/password_reset.html"
    success_url = '/reviews/login'
    form_class = SetPasswordForm

    def form_valid(self,form):
        
        uidb64=self.kwargs['uidb64']
        token=self.kwargs['token']
        UserModel = get_user_model()
        uid = urlsafe_base64_decode(uidb64).decode('utf-8')
        user = UserModel.objects.get(pk=uid)
        if form.is_valid():
            if user is not None:
                if default_token_generator.check_token(user, token):
                    new_password= form.cleaned_data['password']
                    user.set_password(new_password)
                    user.save()
                    messages.success(self.request, 'Password reset successful.')
                    return redirect("configurations:login")
                else:
                    messages.error(self.request, 'Token is not valid!! Please request for password reset again.')
            else:
                messages.error(self.request, 'Password could not be reset!!')

        return render(self.request,'registration/password_reset.html',{'form':form})

    def get_context_data(self, **kwargs):
        context=super(PasswordResetConfirmView,self).get_context_data(**kwargs)
        context['action_button_label']='Reset Password'
        return context