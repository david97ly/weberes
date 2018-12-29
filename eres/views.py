# coding=utf-8
from django.shortcuts import render, get_object_or_404,redirect,get_list_or_404,render_to_response
from django.core.exceptions import ObjectDoesNotExist
from django.template.loader import get_template
from django.template import Context
from django.template.context import RequestContext
from django.core import serializers
from django.http import HttpResponse,HttpResponseRedirect,JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from .forms import *
from django.views.generic import TemplateView, FormView,CreateView, UpdateView
#from django.core.urlresolvers import reverse_lazy, reverse
from .models import *
from random import choice
#from metodos import *
from decimal import Decimal
from datetime import datetime,timedelta
import time
import hashlib
from django.utils import timezone
import pytz
from django.core.mail import EmailMessage
from django.db.models import Q
#from .htmltopdf import render_to_pdf
from datetime import *
from django.template.defaultfilters import slugify
import sys
# Create your views here.

"""reload(sys)  # Reload does the trick!
sys.setdefaultencoding('UTF8')"""

class LogInView(FormView):
    template_name = 'login.html'
    form_class = loginForm
    success_url = '/'

    def form_valid(self,form):


       us = form.cleaned_data['username']
       pas = form.cleaned_data['password']

       us = us.strip()
       pas = pas.strip()

       user = authenticate(username=us, password=pas)

       if user.is_active:
           login(self.request,user)
           return super(LogInView,self).form_valid(form)
       else:
           return redirect('/')

@login_required
def logOut(request):
    logout(request)
    return redirect("/")

class UserRegisterView(CreateView):

    form_class = UserCreateForm
    template_name = "registro.html"
    success_url = '/ingresar'

    def form_valid(self,form):
        user = form.save()
        user.set_password(form.cleaned_data['password'])
        #enviar_email()
        cod = Codigo()
        cod.user = user
        cod.save()

        return super(UserRegisterView,self).form_valid(form)


def corregir(request):
    try:
        print ("antes de hacer todo *-*--*-*-*-*-*-* ")
        user = User.objects.all()
        for u in user:
            try:
                u.username = u.username.strip()
                u.save()
            except Exception as e:
                pass

        return redirect('login')
    except Exception as e:
        return redirect("home")

def home(request):

    titulo = "Pagina principal"
    template = 'landing2.html'
    varible = "Exploradores"


    context = {'variable':varible}

    return render(request,template,context)

@login_required(login_url='ingresar')
def codigo(request):
    try:
        us  = User.objects.get(pk = request.user.id)
        coduse = Codigo.objects.get(user = us)
        if not coduse.codigo == None:
            return redirect("home")

        if request.POST:
            form = CodigoForm(request.POST,instance = us)
            if form.is_valid():
                #codigo = form.save(commit=False)
                #codigo.save()
                print("veamos que imprime")
                print("Significa que si es valido " + str(form.cleaned_data['codigo']))
                print("ya imprimio")
                try:
                    cod = form.cleaned_data['codigo']
                    coduser = Codigo.objects.get(user = us)
                    coduser.codigo = cod
                    coduser.save()
                    form.save()
                except Exception as e:
                    print("NO GUARDO PORQUE: " + str(e))

                return redirect("perfil")
            else:
                print("El formulario no es valido")
                return redirect("home")
        else:
            form = CodigoForm(instance=us)
            template = "acceso.html"
            context = {'form':form}
            return render(request,template,context)


        context = {'us':us}
        template ="acceso.html"
        return render(request,template,context)
    except Exception as e:
        print("Este es el error " + str(e))
        return redirect("home")

@login_required(login_url='ingresar')
def perfil(request):
    try:
        us = User.objects.get(pk = request.user.id)
        cod = Codigo.objects.get(user=us)
        print ("esto tiene codigo " + str(cod.codigo))
        if cod.codigo == None:
            return redirect("codigo")


        context = {'us':us}
        template ="profile.html"
        print("apunto de llegar a profiles")
        return render(request,template,context)
    except Exception as e:
        print (e)
        return redirect("home")


@login_required(login_url='ingresar')
def destacamento(request):
    try:
        us = User.objects.get(pk = request.user.id)
        cod = Codigo.objects.get(user=us)
        print ("esto tiene codigo " + str(cod.codigo))
        if cod.codigo == None:
            return redirect("codigo")
        else:
            context = {'us':us}
            template ="destacamento.html"
            print("apunto de llegar a profiles")

            return render(request,template,context)
    except Exception as e:
        print (e)
