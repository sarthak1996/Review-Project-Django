from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from django.contrib.auth.models import Group
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

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def save_profile(sender, instance, created, **kwargs):
	if created:
		try:
			grp = Group.objects.get(name='Employee')
			instance.groups.add(grp)
		except Exception as e:
			print('Something went wrong while adding default group!')
			print(e)

@receiver(post_save,sender=Choice)
@receiver(post_save,sender=Question)
@receiver(post_save,sender=Series)
@receiver(post_save,sender=Team)
@receiver(post_save,sender=Approval)
@receiver(post_save,sender=Exemption)
@receiver(post_save,sender=Review)
@receiver(post_save,sender=Answer)
def generic_post_save_attribute_initialization(sender,instance,created,**kwargs):
	instance.version=instance.version+1


