from django.views.generic.edit import CreateView 
from configurations.models import Choice
import datetime 
from configurations.forms.ChoiceForm import ChoiceForm
from django.contrib import messages
class ChoiceCreateView(CreateView):
	model= Choice
	form_class=ChoiceForm
	template_name='configurations/create_view.html'

	def form_valid(self, form):
		form.instance.last_update_by=self.request.user
		form.instance.created_by=self.request.user
		form.instance.creation_date=datetime.datetime.now()
		messages.success(self.request, 'Successfully created choice : '+form.instance.choice_text)
		return super().form_valid(form)

	def get_context_data(self, **kwargs):
		context=super(ChoiceCreateView,self).get_context_data(**kwargs)
		context['page_title']='Create Choice'
		context['card_title']='Choice'
		return context