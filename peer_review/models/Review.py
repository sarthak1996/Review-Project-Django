from django.db import models
from django.conf import settings
from configurations.models import Team,Question,Series
from collections import OrderedDict
from django.urls import reverse_lazy
# from peer_review.HelperClasses import ApprovalHelper

REVIEW_PRIORITY=[(1,"High Priority (Sev1)"),(2,"Normal priority (Sev2)")]
APPROVAL_OUTCOMES=[('APR','APPROVED'),('PND','PENDING'),('REJ','REJECTED'),('INV','INVALID')]

class Review(models.Model):
	bug_number = models.CharField(max_length=10,blank=False)
	priority=models.IntegerField(choices=REVIEW_PRIORITY)	
	approval_outcome=models.CharField(max_length=4,blank=False,choices=APPROVAL_OUTCOMES)
	team=models.ForeignKey(Team,related_name='review_team_assoc',on_delete=models.PROTECT)
	creation_date=models.DateTimeField(blank=False)
	last_update_date=models.DateTimeField(auto_now=True)
	created_by=models.ForeignKey(settings.AUTH_USER_MODEL, related_name='reviews_created_by',on_delete=models.PROTECT)
	last_update_by=models.ForeignKey(settings.AUTH_USER_MODEL, related_name='reviews_last_update_by',on_delete=models.PROTECT)
	review_type=models.CharField(max_length=10, blank=False,choices=Question.get_questions_choice_types()['question_type'])
	# num_of_exemption=models.IntegerField(blank=True,default=0) 
	series_type=models.CharField(max_length=3,blank=True,null=True,choices = Series.get_choices_models()['series_type'])
	
	class Meta:
		verbose_name_plural = "Reviews"
	def __str__(self):
		return self.created_by.username + '->' + ' for '+ self.bug_number

	@staticmethod
	def get_review_priority_approval_types():
		return {'review_priority':REVIEW_PRIORITY,
				'approval_outcome':APPROVAL_OUTCOMES}

	def get_values_for_fields(self):
		field_dict=OrderedDict()
		QUESTION_TYPE=Question.get_questions_choice_types()['question_type']
		SERIES_TYPE=Series.get_choices_models()['series_type']
		# field_dict['Team Name']=self.team_name
		field_dict['Bug number']=self.bug_number
		field_dict['Priority']=''.join([value for (item,value) in REVIEW_PRIORITY if item==self.priority])
		field_dict['Approval Outcome']=''.join([value for (item,value) in APPROVAL_OUTCOMES if item==self.approval_outcome])
		field_dict['Review type']=''.join([value for (item,value) in QUESTION_TYPE if item==self.review_type])
		field_dict['Team']=self.team.team_name
		field_dict['Raised to']=self.approval_review_assoc.filter(latest=True).first().raised_to
		# field_dict['Number of exemptionss']=str(self.num_of_exemption)
		field_dict['Series Type']=''.join([value for (item,value) in SERIES_TYPE if item==self.series_type])
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
		return reverse_lazy('peer_review:review_detail_view',kwargs={'obj_pk':self.pk})

	def get_display_list_name(self):
		return self.created_by.username + '->' +' for '+ self.bug_number 

