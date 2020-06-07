from django.db import models
from django.conf import settings
from configurations.models import Team,Question,Series
from collections import OrderedDict
from django.urls import reverse_lazy
from peer_review.HelperClasses import StatusCodes,CommonLookups

# from peer_review.HelperClasses import ApprovalHelper
REVIEW_PRIORITY=CommonLookups.get_review_priorities()
APPROVAL_OUTCOMES=CommonLookups.get_approval_outcomes()

class Review(models.Model):
	bug_number = models.CharField(max_length=10,blank=False)
	priority=models.IntegerField(choices=CommonLookups.get_review_priorities())	
	approval_outcome=models.CharField(max_length=4,blank=False,choices=CommonLookups.get_approval_outcomes())
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
		return {'review_priority':CommonLookups.get_review_priorities(),
				'approval_outcome':CommonLookups.get_approval_outcomes()}

	def get_values_for_fields(self):
		field_dict=OrderedDict()
		QUESTION_TYPE=Question.get_questions_choice_types()['question_type']
		SERIES_TYPE=Series.get_choices_models()['series_type']
		# field_dict['Team Name']=self.team_name
		# field_dict['Bug number']=self.bug_number
		field_dict['Priority']=''.join([value for (item,value) in REVIEW_PRIORITY if item==self.priority])
		field_dict['Approval Outcome']=''.join([value for (item,value) in APPROVAL_OUTCOMES if item==self.approval_outcome])
		field_dict['Review type']=''.join([value for (item,value) in QUESTION_TYPE if item==self.review_type])
		field_dict['Team']=self.team.team_name
		field_dict['Raised to']=self.approval_review_assoc.filter(latest=True).first().raised_to
		# field_dict['Number of exemptionss']=str(self.num_of_exemption)
		field_dict['Series Type']=CommonLookups.get_non_aru_series_type_name() if not self.series_type else self.series_type
		field_dict['Created By']=self.created_by.username
		field_dict['Creation Date']= str(self.creation_date)
		# print(field_dict.items())
		return field_dict.items()

	def get_values_for_fields_answers(self):
		field_dict=OrderedDict()
		answer_obj=self.answer_review_assoc.all()
		for ans in answer_obj:
			field_dict[ans.question.question_text]=ans.answer
		return field_dict.items()

	def get_last_update_fields(self):
		field_dict=OrderedDict()
		field_dict['Last Update By']= self.last_update_by.username
		field_dict['Last Update Date']= str(self.last_update_date)
		return field_dict.items()

	def get_absolute_url(self):
		return reverse_lazy('peer_review:review_detail_view',kwargs={'obj_pk':self.pk})

	def get_display_list_name(self):
		return self.bug_number 

	def is_pending(self):
		return self.approval_outcome==StatusCodes.get_pending_status()

	def get_tag_right_1(self):
		# print('tag_right_1')
		return ''.join([value for (item,value) in APPROVAL_OUTCOMES if item==self.approval_outcome])

	def get_display_list_description(self):
		desc=OrderedDict()
		idx="Team: "+self.team.team_name
		desc[idx]=''.join([value for (item,value) in REVIEW_PRIORITY if item==self.priority])
		idx="Raised to:"+self.approval_review_assoc.get(latest=True).raised_to.get_full_name()
		desc[idx]=None
		return desc.items()

	def get_display_list_continuous_tags(self):
		QUESTION_TYPE=Question.get_questions_choice_types()['question_type']
		SERIES_TYPE=Series.get_choices_models()['series_type']
		review_type=''.join([value for (item,value) in QUESTION_TYPE if item==self.review_type])
		series_type=CommonLookups.get_non_aru_series_type_name() if not self.series_type else self.series_type
		return [review_type,series_type]

	def get_reviews_raised_by_me_actions(self,exclude=None):
		if self.approval_outcome==StatusCodes.get_approved_status():
			return None
		actions=OrderedDict()
		print('Fetching actions allowed on raised by me review')
		print(exclude)
		if not exclude or (exclude and 'update' not in exclude):
			actions['Update']='peer_review:review_update_view'
		if not exclude or (exclude and 'invalidate' not in exclude):
			actions['Invalidate']='peer_review:invalidate_review'
		return actions.items()

	def get_review_raised_to_me_actions(self,exclude=None):
		if self.approval_outcome!=StatusCodes.get_pending_status():
			return None
		actions=OrderedDict()
		print('Fetching actions allowed on raised to me review')
		print(exclude)
		if not exclude or (exclude and 'approve' not in exclude):
			actions['Approve']='peer_review:review_detail_approve_view'
		if not exclude or (exclude and 'reject' not in exclude):
			actions['Reject']='peer_review:reject_review'
		if not exclude or (exclude and 'delegate' not in exclude):
			actions['Delegate']='peer_review:delegate_review'
		return actions.items()

	def get_peer_testing_raised_to_me_actions(self,exclude=None):
		if self.approval_outcome!=StatusCodes.get_pending_status():
			return None
		actions=OrderedDict()
		print('Fetching actions allowed on raised to me review')
		print(exclude)
		if not exclude or (exclude and 'approve' not in exclude):
			actions['Approve']='peer_testing:peer_testing_approve'
		if not exclude or (exclude and 'reject' not in exclude):
			actions['Reject']='peer_review:reject_review'
		if not exclude or (exclude and 'delegate' not in exclude):
			actions['Delegate']='peer_review:delegate_review'
		return actions.items()

