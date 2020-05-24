from django.db import models
from django.conf import settings
from peer_review.models import Review
from configurations.models import Question
class Answer(models.Model):
	review = models.ForeignKey(Review,related_name='answer_review_assoc',blank=False,on_delete=models.PROTECT)
	question=models.ForeignKey(Question,related_name='answer_question_assoc',blank=False,on_delete=models.PROTECT)
	answer=models.CharField(max_length=250,blank=True,null=True)
	creation_date=models.DateTimeField(blank=False)
	last_update_date=models.DateTimeField(auto_now=True)
	created_by=models.ForeignKey(settings.AUTH_USER_MODEL, related_name='answers_created_by',on_delete=models.PROTECT)
	last_update_by=models.ForeignKey(settings.AUTH_USER_MODEL, related_name='answers_last_update_by',on_delete=models.PROTECT)
	class Meta:
		verbose_name_plural = "Answers"
	# def __str__(self):
	# 	return self.question.question_text + ' : '+self.answer

	