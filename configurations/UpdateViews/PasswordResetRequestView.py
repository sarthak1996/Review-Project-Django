from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template import loader
from django.views.generic import FormView
from configurations.forms import PasswordResetRequestForm
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.db.models.query_utils import Q
from peer_review.HelperClasses.EmailHelper import send_email_mutt

class PasswordResetRequestView(FormView):
    template_name = "registration/password_reset.html"
    success_url = '/reviews/login'
    form_class = PasswordResetRequestForm

    def form_valid(self,form):
        
        data= form.cleaned_data["email_or_username"]
        user= get_user_model().objects.filter(Q(email=data)|Q(username=data)).first()
        if user:
            c = {
                'email': user.email,
                'domain': self.request.META['HTTP_HOST'],
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'user': user,
                'token': default_token_generator.make_token(user),
                'protocol': self.request.scheme,
            }
            email_template_name='email/password_reset_email.html'
            subject = "Reset Password Request"
            # body=str(render(self.request,'email/outcome_complete_review_email.html',context))
            email = loader.render_to_string(email_template_name, c)
            try:
                send_email_mutt(to=user.email,
                            cc='',
                            body=email,
                            subject=subject)
                messages.success(self.request,'Email has been sent to '+user.email)
            except Exception as e:
                print(e)
                messages.error(self.request,'Email could not be sent : '+str(e))
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context=super(PasswordResetRequestView,self).get_context_data(**kwargs)
        context['action_button_label']='Send Email'
        return context

