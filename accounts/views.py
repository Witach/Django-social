from django.shortcuts import render
from django.core.urlresolvers import reverse_lazy
from django.views.generic import CreateView
from accounts.form import UserCreateForm
class SignUp(CreateView):
    form_class = UserCreateForm
    success_url  = reverse_lazy("login")
    template_name = "sign_up.html"
# Create your views here.
