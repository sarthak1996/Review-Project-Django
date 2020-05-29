from django.db import models
from django.conf import settings
from collections import OrderedDict 
from django.urls import reverse_lazy
from peer_review.HelperClasses import CommonLookups

class Series(models.Model):
	series_name=models.CharField(max_length=200,blank=False)
	series_type = models.CharField(max_length=3,blank=True,null=True,choices = CommonLookups.get_series_types())
	creation_date=models.DateTimeField(blank=False)
	last_update_date=models.DateTimeField(auto_now=True)
	created_by=models.ForeignKey(settings.AUTH_USER_MODEL, related_name='series_created_by',on_delete=models.PROTECT)
	last_update_by=models.ForeignKey(settings.AUTH_USER_MODEL, related_name='series_last_update_by',on_delete=models.PROTECT)
	class Meta:
		verbose_name_plural = "Series"

	def __str__(self):
		return self.series_name

	@staticmethod
	def get_choices_models():
		return {'series_type':CommonLookups.get_series_types()}

	def get_values_for_fields(self):
		field_dict=OrderedDict()
		# field_dict['Team Name']=self.team_name
		field_dict['Series type']=SERIES_TYPE[1][1] if not self.series_type else self.series_type
		field_dict['Created By']=self.created_by.username
		field_dict['Creation Date']= str(self.creation_date)
		# print(field_dict.items())
		return field_dict.items()

	def get_last_update_fields(self):
		field_dict=OrderedDict()
		field_dict['Last Update By']= self.last_update_by.username
		field_dict['Last Update Date']= str(self.last_update_date)
		return field_dict.items()

	def get_absolute_url(self):
		return reverse_lazy('configurations:series_detail_view',kwargs={'obj_pk':self.pk})

	def get_display_list_name(self):
		return self.series_name
