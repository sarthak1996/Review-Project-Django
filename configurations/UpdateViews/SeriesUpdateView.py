from django.views.generic.edit import UpdateView 
from configurations.models import Series
from configurations.forms.SeriesForm import SeriesForm

class SeriesUpdateView(UpdateView):
	model=Series
	template_name='configurations/create_view.html'
	# fields=[
	# 	'series_name',
	# 	'series_type',
	# ]
	form_class=SeriesForm
	pk_url_kwarg='obj_pk'

	def form_valid(self, form):
		form.instance.last_update_by=self.request.user
		return super().form_valid(form)

	def get_context_data(self, **kwargs):
		context=super(SeriesUpdateView,self).get_context_data(**kwargs)
		context['page_title']='Update Series'
		context['card_title']='Series'
		return context