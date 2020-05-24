from django.db import models
from django.contrib.auth.models import AbstractUser
from .Team import Team

class User(AbstractUser):
	team=models.ForeignKey(Team,on_delete=models.PROTECT,related_name='user_team_assoc',null=True,blank=True)
