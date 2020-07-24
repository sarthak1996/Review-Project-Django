from django.db.models.signals import post_save,pre_save
from django.dispatch import receiver
from django.conf import settings
from django.contrib.auth.models import Group
from configurations.HelperClasses import LoggingHelper
import traceback
from django_currentuser.middleware import get_current_authenticated_user
from django.utils import timezone
from configurations.models import (	
	Choice,	
	Question,	
	Series,	
	Team	
)	
from peer_review.models import(	
	Approval,	
	Exemption,	
	Review	
)	
from peer_testing.models import Answer
from configurations.HelperClasses import LoggingHelper

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def save_profile(sender, instance, created, **kwargs):
	if created:
		try:
			grp = Group.objects.get(name='Employee')
			instance.groups.add(grp)
		except Exception as e:
			logger=LoggingHelper(instance,__name__)
			logger.write('Something went wrong while adding default group!',LoggingHelper.DEBUG)
			logger.write(str(traceback.format_exc()),LoggingHelper.DEBUG)


@receiver(pre_save,sender=Choice)	
@receiver(pre_save,sender=Question)	
@receiver(pre_save,sender=Series)	
@receiver(pre_save,sender=Team)	
@receiver(pre_save,sender=Approval)	
@receiver(pre_save,sender=Exemption)	
@receiver(pre_save,sender=Review)	
@receiver(pre_save,sender=Answer)
def update_who_columns(sender,instance,**kwargs):
	is_created=sender.objects.filter(pk=instance.pk).count()==0
	user=get_current_authenticated_user()
	logger=LoggingHelper(user,__name__)
	curr_time=timezone.now()
	
	
	#check for seed data
	if instance.created_by is not None and instance.last_update_by is not None and instance.created_by==instance.last_update_by:
		user = instance.created_by
	logger.write('Pre save signal',LoggingHelper.DEBUG)	
	logger.write('Request user: '+str(user.username),LoggingHelper.DEBUG)
	logger.write('Is created: '+str(is_created),LoggingHelper.DEBUG)
	logger.write('Timestamp: '+str(curr_time),LoggingHelper.DEBUG)
	
	if is_created:
		instance.creation_date=curr_time
		instance.created_by=user
	instance.last_update_by=user		



