from django.contrib import admin
from .models import Team,User,Choice,Question,Series
# Register your models here.
admin.site.register(Team)
admin.site.register(User)
admin.site.register(Choice)
admin.site.register(Question)
admin.site.register(Series)