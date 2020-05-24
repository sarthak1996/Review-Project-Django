from django.views.generic.edit import CreateView 
from configurations.models import Series
import datetime 
from configurations.forms.SeriesForm import SeriesForm
class SeriesCreateView(CreateView):
	model= Series
	form_class=SeriesForm
	template_name='configurations/create_view.html'

	def form_valid(self, form):
		form.instance.last_update_by=self.request.user
		form.instance.created_by=self.request.user
		form.instance.creation_date=datetime.datetime.now()
		return super().form_valid(form)

	def get_context_data(self, **kwargs):
		context=super(SeriesCreateView,self).get_context_data(**kwargs)
		context['page_title']='Create Series'
		context['card_title']='Series'
		return context