"""weberes URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))



from django.urls import include, re_path

urlpatterns = [
    re_path(r'^index/$', views.index, name='index'),
    re_path(r'^bio/(?P<username>\w+)/$', views.bio, name='bio'),
    re_path(r'^weblog/', include('blog.urls')),
    ...
]
https://docs.djangoproject.com/en/2.1/ref/urls/#path


"""
from django.conf.urls import include, url
from django.contrib.auth.decorators import login_required, permission_required
from django.conf import settings
from django.contrib import admin
from eres.views import *

from django.urls import path,re_path



urlpatterns = [
    path('admin/',admin.site.urls),
    re_path(r'^ingresar/$', LogInView.as_view(), name='login'),
    re_path(r'^logOut', logOut, name='logOut'),
    re_path(r'^registrar/$', UserRegisterView.as_view(), name='registrarme'),
    #path('',home),
    re_path(r'^$', home, name='home'),
]
