from django.views.generic.edit import UpdateView 
from configurations.models import Choice
from configurations.forms.ChoiceForm import ChoiceForm
from django.contrib import messages

class ChoiceUpdateView(UpdateView):
	model=Choice
	template_name='configurations/create_view.html'
	# fields=[
	# 	'choice_text',
	# ]
	form_class=ChoiceForm
	pk_url_kwarg='obj_pk'

	def form_valid(self, form):
		form.instance.last_update_by=self.request.user
		messages.success(self.request, 'Successfully updated choice : '+form.instance.choice_text)
		return super().form_valid(form)

	def get_context_data(self, **kwargs):
		context=super(ChoiceUpdateView,self).get_context_data(**kwargs)
		context['page_title']='Update Choice'
		context['card_title']='Choice'
		return context