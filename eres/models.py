# coding=utf-8
from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.conf import settings
from datetime import datetime,timedelta
import time
from django.utils import timezone
import sys

# sys.setdefaultencoding() does not exist, here!
#reload(sys)  # Reload does the trick!
#sys.setdefaultencoding('UTF8')
# Create your models here.

# Create your models here.

class UserManager(BaseUserManager, models.Manager):

    def _create_user(self, username,email,password, is_staff,is_superuser,**extra_fields):
        email = self.normalize_email(email)
        #if not email:
        #    raise ValueError('El email es obligatorio')
        us = username.strip()
        pas = password.strip()

        user = self.model(username=us,email=email,is_active=True,is_staff=is_staff,is_superuser = is_superuser, **extra_fields)

        user.set_password(pas)
        user.save(using = self._db)
        return user

    def create_user(self, username,email,password=None,**extra_fields):
        us = username.strip()
        pas = password.strip()
        return self._create_user(us,email,pas,False,False,**extra_fields)

    def create_superuser(self, username,email,password,**extra_fields):
        return self._create_user(username,email,password,True,True,**extra_fields)


class User(AbstractBaseUser,PermissionsMixin):
    username = models.CharField(unique=True, max_length=50)
    email = models.EmailField(unique=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email'] #no necestitamos campos obligatorios

    def get_short_name(self):
        return self.username
