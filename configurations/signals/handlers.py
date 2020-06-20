from django.db.models.signals import post_save,pre_save
from django.dispatch import receiver
from django.conf import settings
from django.contrib.auth.models import Group
from configurations.Exceptions import OptimisticLockingException
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



@receiver(pre_save,sender=Choice)
@receiver(pre_save,sender=Question)
@receiver(pre_save,sender=Series)
@receiver(pre_save,sender=Team)
@receiver(pre_save,sender=Approval)
@receiver(pre_save,sender=Exemption)
@receiver(pre_save,sender=Review)
@receiver(pre_save,sender=Answer)
def optimistic_locking(sender,instance,**kwargs):
	is_created=sender.objects.filter(pk=instance.pk).count()==0
	print('Pre save signal')
	print(is_created)
	if not is_created:
		row_count=sender.objects.filter(pk=instance.pk,
									version=instance.version).count()
		print(row_count,instance.version,sender.objects.filter(pk=instance.pk).first().version)
		if row_count != 1:
			raise OptimisticLockingException
		else:
			instance.version=instance.version+1



