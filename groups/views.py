from django.shortcuts import render
from django.views import generic
from .models import Group,Membership
from django.db import IntegrityError
from django.contrib import messages
from django.shortcuts import get_object_or_404
from accounts.models import User
from django.urls import reverse
import groups.models as models
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
# Create your views here.
class CreateGroup(LoginRequiredMixin,generic.CreateView):
    fields = ("name" , "description" )
    model = Group

class SingleGroup(generic.DetailView):
    model = Group
    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        print(len(Membership.objects.filter(user__pk=request.user.pk,group__slug=self.kwargs.get("pk"))))
        if len(Membership.objects.filter(user__pk=request.user.pk,group__slug=self.kwargs.get("slug")))>=1:
            return render(request,"groups/group_detail0.html",context)
        else:
            return self.render_to_response(context)


class ListGroups(generic.ListView):
    model = Group

class JoinGroup(LoginRequiredMixin,generic.RedirectView):

    def get_redirect_url(self, *args, **kwargs ):
        return reverse("groups:single",kwargs={"slug":self.kwargs.get("slug")})

    def get(self, request, *args , **kwargs):
        group = get_object_or_404(Group,slug=self.kwargs.get("slug"))

        try:
            print(self.request.user.username)
            print("*"*5,User.objects.get(username=self.request.user.username),"*"*5)
            Membership.objects.create(user=User.objects.get(pk=self.request.user.pk),group=group)
        except IntegrityError:
            messages.warning(self.request,"warning you're arleady a member of {}".format(group.name))
        else:
            messages.success(self.request,"You are now a member of the {} group".format(group.name))
        return super().get(request,*args,**kwargs)

class LeaveGroup(LoginRequiredMixin, generic.RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        return reverse("groups:single",kwargs={"slug":self.kwargs.get("slug")})

    def get(self, request, *args, **kwargs):

        try:
            memberships = models.Membership.objects.filter(user=self.request.user,group__slug=self.kwargs.get("slug")).get()
        except models.Membership.DoesNotExist:
            messages.warning(self.request,"You are not in group")
        else:
            memberships.delete()
            messages.success(self.request,"You have succesfully left group")
        return super().get(request, *args, **kwargs)
