from django.db import models
from django.conf import settings
from collections import OrderedDict 
from django.urls import reverse_lazy

class Team(models.Model):
	team_name=models.CharField(max_length=20,blank=False)
	team_grp_mail=models.EmailField(max_length = 254,null=True,blank=True)
	creation_date=models.DateTimeField(blank=False)
	last_update_date=models.DateTimeField(auto_now_add=True)
	created_by=models.ForeignKey(settings.AUTH_USER_MODEL, related_name='teams_created_by',on_delete=models.PROTECT)
	last_update_by=models.ForeignKey(settings.AUTH_USER_MODEL, related_name='teams_last_update_by',on_delete=models.PROTECT)
	class Meta:
		verbose_name_plural = "Teams"
	def __str__(self):
		return self.team_name
	def get_values_for_fields(self):
		field_dict=OrderedDict()
		# field_dict['Team Name']=self.team_name
		field_dict['Team Group Email']=self.team_grp_mail
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
		return reverse_lazy('configurations:team_detail_view',kwargs={'obj_pk':self.pk})

	def get_display_list_name(self):
		return self.team_name
