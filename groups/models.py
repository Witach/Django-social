from django.db import models
from django.config import settings
from django.core.urlresolvers import reverse
from django.utils.text import slugify
from django.contrib.auth import get_user_model
from django import template
# Create your models hereself.
User = get_user_model()
register = template.Library()


class Group(models.Model):
    name = models.CharField(max_length=32,unique=True)
    slug = models.SlugField(allow_unicode=True, unique=True)
    description = models.TextField(blank=True, default='')
    desription_html=models.TextField(editable=False,blank=True, default='')
    members =model.ManyToManyField(through="Membership")

    def __str__(self):
        return self.name

    def save(self,*arg,**kwargs):
        self.slug = slugify(self.name)
        self.description_html = self.description
        super().save(*args,**kwargs)

    def get_absolute_url(self):
        return reverse("groups:single",kwargs={"slug":self.slug})

    class Meta():
        ordering = ["name"]

class Membership(models.Model):
    group = models.ForeignKey(Group , related_name="memberships")
    user = models.ForeignKey(User , related_name='user_groups')

    def __str__(self):
        return self.user.username

    class Meta():
        unique_together = ( "group" , "user" )
