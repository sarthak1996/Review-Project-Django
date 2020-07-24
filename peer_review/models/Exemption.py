from django.db import models
from django.conf import settings
from .Review import Review
from concurrency.fields import IntegerVersionField
class Exemption(models.Model):
	review=models.ForeignKey(Review,related_name='exemption_review_assoc',blank=False,on_delete=models.PROTECT)
	exemption_for= models.CharField(max_length=250,blank=False)
	exemption_explanation=models.CharField(max_length=1000,blank=False)
	creation_date=models.DateTimeField(blank=False)
	last_update_date=models.DateTimeField(auto_now=True)
	created_by=models.ForeignKey(settings.AUTH_USER_MODEL, related_name='exemptions_created_by',on_delete=models.PROTECT)
	last_update_by=models.ForeignKey(settings.AUTH_USER_MODEL, related_name='exemptions_last_update_by',on_delete=models.PROTECT)
	version = IntegerVersionField()
	class Meta:
		verbose_name_plural = "Exemptions"
		db_table="prv_exemptions"
	def __str__(self):
		return self.review.bug_number + '->' + self.exemption_for+'->' +self.exemption_explanation