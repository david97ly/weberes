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

from django.views.static import serve


urlpatterns = [
    path('admin/',admin.site.urls),
    re_path(r'^ingresar/$', LogInView.as_view(), name='login'),
    re_path(r'^logOut', logOut, name='logOut'),
    re_path(r'^registro/$', UserRegisterView.as_view(), name='registro'),
    re_path(r'^corregir', corregir, name='corregir'),
    re_path(r'^perfil',perfil, name='perfil'),
    re_path(r'^asignarcargo',asignarcargo, name='asignarcargo'),
    re_path(r'^infoperfil/(?P<idperfil>\d+)$',infoperfil, name='infoperfil'),
    re_path(r'^errorcodigo',errorcodigo, name='errorcodigo'),
    re_path(r'^exploblog',exploblog, name='exploblog'),
    re_path(r'^utilierrorcodigo',utilierrorcodigo, name='utilierrorcodigo'),
    re_path(r'^codigo',codigo, name='codigo'),
    re_path(r'^destacamento',destacamento, name='destacamento'),
    re_path(r'^inscripcion/(?P<iddesta>\d+)$',inscripcion, name='inscripcion'),
    re_path(r'^registroexplorador/(?P<iddesta>\d+)$', registroexplorador, name='registroexplorador'),
    re_path(r'^editarexplorador/(?P<iddesta>\d+)/(?P<idexplo>\d+)$', editarexplorador, name='editarexplorador'),
    re_path(r'^permisoeditarexplorador/(?P<iddesta>\d+)/(?P<idexplo>\d+)$', permisoeditarexplorador, name='permisoeditarexplorador'),
    re_path(r'^admindestacamento/(?P<iddesta>\d+)$',admindestacamento, name='admindestacamento'),
    re_path(r'^zonadestacamentos/(?P<idzona>\d+)$',zonadestacamentos, name='zonadestacamentos'),
    re_path(r'^zonas',zonas, name='zonas'),
    re_path(r'^creardestacamento',login_required(CrearDestacamentoView.as_view(),login_url='login'), name='creardestacamento'),
    re_path(r'^editardestacamento/(?P<idzona>\d+)$', editardestacamento, name='editardestacamento'),
    re_path(r'^detalledestacamento/(?P<iddesta>\d+)$', detalledestacamento, name='detalledestacamento'),
    re_path(r'^setfechajax/$',login_required(SetFecha.as_view(),login_url='login'),name='setearfecha'),
    re_path(r'^buscarexplo/$',login_required(BuscarExplo.as_view(),login_url='login'),name='buscarexplo'),
    re_path(r'^enviarmajax/$',login_required(MensajeEnviar.as_view(),login_url='login'),name='enviarmajax'),
    #re_path(r'^recibirmajax/$',login_required(MensajeRecibir.as_view(),login_url='login',name = 'recibirmajax')),
    re_path(r'^block/$',login_required(Block.as_view(),login_url='login'),name='block'),
    re_path(r'^ajaxcargos/$',login_required(CargoAjax.as_view(),login_url='login'),name='ajaxcargos'),
    

    #path('',home),
    re_path(r'^$', home, name='home'),
    re_path(r'^media/(?P<path>.*)$', serve,{'document_root': settings.MEDIA_ROOT,}),
]
