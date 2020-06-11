from django.db import models
from django.conf import settings
from collections import OrderedDict 
from django.urls import reverse_lazy
from .Choice import Choice
from peer_review.HelperClasses import CommonLookups

class Question(models.Model):
	question_text=models.CharField(max_length=200,blank=False)
	question_choice_type=models.CharField(max_length=3, blank=False,choices=CommonLookups.get_question_choice_types())
	mandatory=models.BooleanField(blank=True)
	creation_date=models.DateTimeField(blank=False)
	last_update_date=models.DateTimeField(auto_now=True)
	series_type=models.CharField(max_length=3,blank=True,null=True,choices = CommonLookups.get_series_types())
	created_by=models.ForeignKey(settings.AUTH_USER_MODEL, related_name='questions_created_by',on_delete=models.PROTECT)
	last_update_by=models.ForeignKey(settings.AUTH_USER_MODEL, related_name='question_last_update_by',on_delete=models.PROTECT)
	choices=models.ManyToManyField(Choice,blank=True,related_name='question_choices_assoc')
	question_type=models.CharField(max_length=10, blank=False,choices=CommonLookups.get_question_types())
	
	class Meta:
		verbose_name_plural = "Questions"
	def __str__(self):
		return self.question_text

	@staticmethod
	def get_questions_choice_types():
		return {'question_type':CommonLookups.get_question_types(),
			'question_choice_type':CommonLookups.get_question_choice_types()}

	def get_values_for_fields(self):
		field_dict=OrderedDict()
		SERIES_TYPE=CommonLookups.get_series_types()
		QUESTION_CHOICE_TYPE=CommonLookups.get_question_choice_types()
		QUESTION_TYPE=CommonLookups.get_question_types()
		# field_dict['Team Name']=self.team_name
		# field_dict['Question text']=self.question_text
		field_dict['Question choice type']=''.join([value for (item,value) in QUESTION_CHOICE_TYPE if item==self.question_choice_type])
		field_dict['Mandatory']=self.mandatory
		field_dict['Question type']=''.join([value for (item,value) in QUESTION_TYPE if item==self.question_type])
		field_dict['Series type']=SERIES_TYPE[1][1] if not self.series_type else self.series_type
		field_dict['MULTI_DISP_FIELD']='Choices'
		field_dict['Created By']=self.created_by.username
		field_dict['Creation Date']= str(self.creation_date)
		# print(field_dict.items())
		return field_dict.items()

	#create method to return choice list for rendering
	def get_choices_multi_field(self):
		choice_list=self.choices.all()
		return [choice for choice in choice_list]


	def get_last_update_fields(self):
		field_dict=OrderedDict()
		field_dict['Last Update By']= self.last_update_by.username
		field_dict['Last Update Date']= str(self.last_update_date)
		return field_dict.items()

	def get_absolute_url(self):
		return reverse_lazy('configurations:question_detail_view',kwargs={'obj_pk':self.pk})

	def get_display_list_name(self):
		return self.question_text
		
	def get_tag_right_1(self):
		return 'Mandatory' if self.mandatory else None

	def get_display_list_description(self):
		QUESTION_CHOICE_TYPE=CommonLookups.get_question_choice_types()
		QUESTION_TYPE=CommonLookups.get_question_types()
		SERIES_TYPE=CommonLookups.get_series_types()
		desc=OrderedDict()
		idx='Series: '+ SERIES_TYPE[1][1] if not self.series_type else self.series_type
		desc[idx]=None
		idx='Choice type: '+''.join([value for (item,value) in QUESTION_CHOICE_TYPE if item==self.question_choice_type])
		desc[idx]=''.join([value for (item,value) in QUESTION_TYPE if item==self.question_type])
		return desc.items()
		
	def get_display_list_continuous_tags(self):
		choices=self.get_choices_multi_field()
		return [choice.choice_text for choice in choices]

	def get_actions_drop(self):
		return {'Update':'configurations:question_update_view'}.items()
	