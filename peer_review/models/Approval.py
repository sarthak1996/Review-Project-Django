from django.db import models
from django.conf import settings
from .Review import Review
from concurrency.fields import IntegerVersionField
class Approval(models.Model):
	review=models.ForeignKey(Review,related_name='approval_review_assoc',on_delete=models.PROTECT)
	raised_by=models.ForeignKey(settings.AUTH_USER_MODEL, related_name='approval_raised_by',on_delete=models.PROTECT)
	raised_to=models.ForeignKey(settings.AUTH_USER_MODEL, related_name='approval_raised_to',on_delete=models.PROTECT)
	approver_comment=models.CharField(max_length=1000,blank=True,null=True)
	approval_outcome=models.CharField(max_length=4,blank=False,choices=Review.get_review_priority_approval_types()['approval_outcome'])
	delegated=models.BooleanField(blank=True)
	latest=models.BooleanField(blank=True)
	creation_date=models.DateTimeField(blank=False)
	last_update_date=models.DateTimeField(auto_now_add=True)
	created_by=models.ForeignKey(settings.AUTH_USER_MODEL, related_name='approvals_created_by',on_delete=models.PROTECT)
	last_update_by=models.ForeignKey(settings.AUTH_USER_MODEL, related_name='approvals_last_update_by',on_delete=models.PROTECT)
	version = IntegerVersionField()

	class Meta:
		verbose_name_plural = "Approvals"
		db_table="prv_approval"

	def __str__(self):
		if self.review:
			return self.review.bug_number+'->'+self.review.review_type