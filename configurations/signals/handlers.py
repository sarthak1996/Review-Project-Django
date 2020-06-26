from django.db.models.signals import post_save,pre_save
from django.dispatch import receiver
from django.conf import settings
from django.contrib.auth.models import Group
from configurations.HelperClasses import LoggingHelper
import traceback

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






