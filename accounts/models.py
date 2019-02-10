from django.db import models
from django.auth import auth

class User(auth.model.User,auth.model.PermissionsMixin):

    def __str__(self):
        return "@{}".format(self.username)
