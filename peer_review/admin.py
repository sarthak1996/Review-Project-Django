from django.contrib import admin
from .models import Review, Approval, Exemption
# Register your models here.

admin.site.register(Review)
admin.site.register(Approval)
admin.site.register(Exemption)
