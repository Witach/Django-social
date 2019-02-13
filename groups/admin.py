from django.contrib import admin
from groups import models
# Register your models here.
class GroupMemberInline(admin.TabularInline):
    model = models.Membership



admin.site.register(models.Group)
admin.site.register(models.Membership)
