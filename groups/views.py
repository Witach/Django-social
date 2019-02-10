from django.shortcuts import render
from django.views import generic
from .models import Group,Membership
from django.db import IntegrityError
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
# Create your views here.
class CreteView(LoginRequiredMixin,generic.CreateView):
    fields = ("name" , "description" )
    model = Group

class SingleGroup(generic.DetailView):
    model = Group

class ListGroup(generic.ListView):
    model = Group

class JoinGroup(LoginRequiredMixin,generic.RedirectView):

    def get_redirect_url(self, *args, **kwargs ):
        return reverse("groups:single",kwargs={"slug":self.kwargs.get("slug")})

    def get(self, request, *args , **kwargs):
        group = get_object_or_404(Group,self.kwargs.get("slug"))

        try:
            Membership.objects.create(user=self.request.user,group=group)
        except IntegrityError:
            messages.warning(self.request,"warning you're arleady a member of {}".format(group.name))
        else:
            message.succes(self.request,"You are now a member of the {} group".format(group.name))
        return super().get(request,*args,**kwargs)

class LeaveGroup(LoginRequiredMixin, generic.RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        return reverse("group:single",kwargs={"slug",self.kwargs.get("slug")})

    def get(self, request, *args, **kwargs):

        try:
            memberships = models.GroupMember.objects.filter(user=self.request.user,group__slug=self.kwargs.get("slug")).get()
        except models.GroupMember.DoesNotExist:
            message.warning(self.request,"You are not in group")
        else:
            membership.delete()
            message.succes(self.requestm,"You have succesfully left group")
        return super.get(request, *args, **kwargs)
