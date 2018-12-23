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
    success_url = reverse_lazy('corregir')

    def form_valid(self,form):


        user = form.save()
        user.set_password(form.cleaned_data['password'])


        #enviar_email()

        return super(UserRegisterView,self).form_valid(form)

def home(request):

    titulo = "Pagina principal"
    template = 'eventos.html'
    varible = "Exploradores"


    context = {'variable':varible}

    return render(request,template,context)
