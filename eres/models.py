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
    foto = models.ImageField(upload_to='avatares',blank=True, null=True)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email'] #no necestitamos campos obligatorios

    def get_short_name(self):
        return self.username

class Codigo(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    codigo = models.CharField(max_length=500,null=True,blank=True)

    def __str__(self):
        return str(self.user.username) + str(" - ") + str(self.codigo)

class Cargos(models.Model):
    nombre = models.CharField(max_length=500,null=True,blank=True)
    codigo = models.IntegerField(blank=True,null=True)
    nivel = models.IntegerField(blank=True,null=True)
    usado = models.BooleanField(default=False)

    def __str__(self):
        return str(self.nombre) + str(" - ") + str(self.nivel) + str(" - ") + str(self.codigo) + str(" - ") + str(self.usado)




class Zona(models.Model):
    nombre = models.CharField(max_length=500,unique=True,blank=True,null=True)
    numero = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return str(self.nombre)

class Destacamento(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,null=True,blank=True,on_delete=models.CASCADE)
    nombre = models.CharField(max_length=500,unique=True,blank=True,null=True)
    codigo = models.IntegerField(blank=True, null=True)
    iglesia = models.CharField(max_length=500,unique=True,blank=True,null=True)
    pastor = models.CharField(max_length=500,unique=True,blank=True,null=True)
    direccion = models.CharField(max_length=500,unique=True,blank=True,null=True)
    direccion_GPS = models.CharField(max_length=500,unique=True,blank=True,null=True)
    zona =  models.ForeignKey(Zona,null=True,on_delete=models.SET_NULL)
    foto = models.ImageField(max_length=1000,blank=True, null=True)

    def __str__(self):
        return self.nombre


class ImagenDestacamento(models.Model):
    imagen = models.ImageField(upload_to='avatares',default="avatares/usuario.png")
    destacamento = models.ForeignKey(Destacamento,null=False,on_delete=models.CASCADE)

    def __str__(self):
        return self.destacamento.nombre


class Perfil(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,null=True,blank=True,on_delete=models.CASCADE)
    cargo = models.ForeignKey(Cargos,null=True,blank=True,on_delete=models.SET_NULL)
    destacamento = models.ForeignKey(Destacamento,null=True,blank=True,on_delete=models.SET_NULL)
    codigo = models.CharField(max_length=500,null=True,blank=True)
    primer_nombre = models.CharField(max_length=500,null=True,blank=True)
    segundo_nombre = models.CharField(max_length=500,null=True,blank=True)
    primer_apellido = models.CharField(max_length=500,null=True,blank=True)
    segundo_apellido = models.CharField(max_length=500,null=True,blank=True)
    sexo = models.CharField(max_length=500,blank=True, null=True)
    telefono = models.CharField(max_length=500,null=True,blank=True)
    direccion = models.CharField(max_length=500,null=True,blank=True)
    direccion_GPS = models.CharField(max_length=500,null=True,blank=True)
    dia = models.IntegerField(blank=True, null=True)
    mes = models.CharField(max_length=500,blank=True, null=True)
    year = models.IntegerField(blank=True, null=True)
    creado = models.DateField(auto_now_add=True)
    foto = models.ImageField(upload_to='avatares',default="static/imagenes/usuario.png",blank=True, null=True)
    activo = models.BooleanField(default=True)
    departamento = models.CharField(max_length=500,null=True,blank=True)


    def __str__(self):
        return str(self.primer_nombre)


class Publicacion(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,null=True,blank=True,on_delete=models.CASCADE)
    fecha = models.DateField(auto_now_add=True,null=True,blank=True)
    tiempo = models.TimeField(auto_now_add=True,null=True,blank=True)
    fechahora = models.DateTimeField(auto_now_add=True,null=True,blank=True)
    titulo = models.CharField(max_length=500,null=True,blank=True)
    descripcion = models.CharField(max_length=10000,null=True,blank=True)
    vistas = models.IntegerField(blank=True, null=True)
    comentarios = models.IntegerField(blank=True, null=True)
    favoritos = models.IntegerField(blank=True, null=True)
    foto = models.ImageField(upload_to='avatares',blank=True, null=True)

    def __str__(self):
        return str(self.descripcion)
