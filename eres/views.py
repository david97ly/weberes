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
from eres.metodos import *
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

@login_required(login_url='login')
def codigo(request):
    try:
        us  = User.objects.get(pk = request.user.id)

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

                    try:
                        per = Perfil.objects.get(codigo = cod)
                        per.user = us
                        per.save()

                    except Exception as e:
                        return redirect("home")
                    else:
                        codn = Codigo()
                        codn.codigo = cod
                        codn.user = us
                        codn.save()

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

@login_required(login_url='login')
def perfil(request):
    try:
        try:
            us = User.objects.get(pk = request.user.id)
            cod = Codigo.objects.get(user=us)
        except Exception as e:
            return redirect("codigo")

        print ("esto tiene codigo " + str(cod.codigo))
        if cod.codigo == None:
            return redirect("codigo")
        else:
            per = Perfil.objects.get(user = us)
            context = {'us':us,'per':per}
            template ="profile.html"
            print("apunto de llegar a profiles")
            return render(request,template,context)
    except Exception as e:
        print (e)
        return redirect("home")


@login_required(login_url='login')
def destacamento(request):
    try:
        us = User.objects.get(pk = request.user.id)
        cod = Codigo.objects.get(user=us)
        print ("esto tiene codigo " + str(cod.codigo))
        if cod.codigo == None:
            return redirect("codigo")
        else:
            context = {'us':us}
            template ="crear-destacamento.html"
            print("apunto de llegar a profiles")

            return render(request,template,context)
    except Exception as e:
        print (e)

class CrearDestacamentoView(CreateView):
    idt = 0

    form_class = DestacamentoForm
    template_name = "registrar-destacamento.html"
    print ("que paso aqui porque dio error")
    success_url = "/admindestacamento"

    def form_valid(self,form):
        print ("significa que el formulario es valido________________")
        form.instance.user = self.request.user

        return super(CrearDestacamentoView,self).form_valid(form)


@login_required(login_url='login')
def admindestacamento(request):
    try:
        us = User.objects.get(pk = request.user.id)
        cod = Codigo.objects.get(user=us)
        explo = False
        print ("esto tiene codigo " + str(cod.codigo))
        if cod.codigo == None:
            return redirect("codigo")
        else:
            try:
                try:
                    destacamento = Destacamento.objects.get(user = request.user)
                except Exception as e:
                    return redirect("/creardestacamento")
                else:
                    explo = Perfil.objects.filter(destacamento=destacamento).exclude(primer_nombre=' ')

                    lisexplo = []
                    class Exp():
                        nombre =""
                        direc = ""
                        foto = ""
                        edad = 0
                        cargo = ""
                        codigo = ""
                    print ("atnes de llegar a la carga a ala lista")
                    for ex in explo:
                        l = Exp()
                        if ex.primer_nombre != None:
                            l.nombre += ex.primer_nombre

                        if ex.segundo_nombre != None:
                            l.nombre += str(" ") + str(ex.segundo_nombre)

                        if ex.primer_apellido != None:
                            l.nombre += str(" ") + str(ex.primer_apellido)

                        if ex.segundo_apellido != None:
                            l.nombre += str(" ") + str(ex.segundo_apellido)


                        l.direc = ex.direccion
                        l.foto = ex.foto.url
                        l.codigo = ex.codigo
                        l.edad = calculedad(ex.dia,ex.mes,ex.year)

                        lisexplo.append(l)

                    print (lisexplo)



            except Exception as e:
                print("No tiene destacamento " + str(e) )


            context = {'us':us,'destacamento':destacamento,'lisexplo':lisexplo}
            template ="lista.html"
            print("apunto de llegar a profiles")

            return render(request,template,context)
    except Exception as e:
        print (e)


@login_required(login_url='login')
def registroexplorador(request,iddesta):
    try:
        desta = Destacamento.objects.get(pk=iddesta)
        perf = Perfil.objects.get(primer_nombre=' ',destacamento=desta)

    except Exception as e:
        perf = Perfil()
        perf.destacamento = desta
        perf.primer_nombre=' '
        perf.year = 1990
        perf.dia = 1
        perf.mes = 1
        perf.save()


    try:
        if request.POST:
            form = PerfilForm(request.POST,request.FILES,instance=perf)
            if form.is_valid():
                fo = form.save(commit=False)
                codigo = ""
                if fo.primer_nombre != None:
                    codigo += fo.primer_nombre[0]

                if fo.segundo_nombre != None:
                    codigo += fo.segundo_nombre[0]

                if fo.primer_apellido != None:
                    codigo += fo.primer_apellido[0]

                if fo.segundo_apellido != None:
                    codigo += fo.segundo_apellido[0]

                print("ESTE ES EL CODIGO: " + str(codigo))

                siglasz = siglas(desta.zona.nombre)
                des = str(siglas( str(str(desta.nombre))))
                codigo = minus(str(codigo))
                ncodigo = generarnumeros(str(str(siglasz) + str(des) + str(codigo)))

                fo.codigo = str(siglasz) + str(des) + str(desta.codigo) + str(codigo) + str(ncodigo)

                fo.save()
                return redirect("/admindestacamento")
        else:
            tp = ''
            n = 1910
            form = PerfilForm(instance=perf)
            template = 'Sign_Up.html'

            context = {'form':form,'n':n,'tp':tp,'perf':perf}

        return render(request,template,context)
    except Exception as e:
        raise

class SetFecha(TemplateView):
    print ("SIQUIERA ENTRE AQUI AL AJAX")
    try:
        def get(self,request,*args,**kwargs):
            print ("YA ENTRE AL METODO HABER QUE PASA AQUI")
            user = request.user
            print ("vEAMOS COMO VA HASTA AQUI")
            print (user)
            fecha = request.GET['fecha']
            indicador = request.GET['indicador']
            user = request.GET['iduser']

            fl = True
            try:

                per = Perfil.objects.get(pk=user)
            except Exception as e:

                fl = False
            else:
                if str(indicador) == 'year':
                    per.year = fecha
                    per.save()
                elif str(indicador) == 'dia':
                    per.dia = fecha
                    per.save()
                elif str(indicador) == 'mes':
                    per.mes = fecha
                    per.save()
                elif str(indicador) == 'hombre':
                    per.sexo =  'Hombre'
                    per.save()
                elif str(indicador) == 'mujer':
                    per.sexo = 'Mujer'
                    per.save()
                elif str(indicador) == 'nuevo' or str(indicador) == 'usado' or str(indicador) == 'reacondicionado':
                    prod = Articulo.objects.get(pk = request.GET['idprod'])
                    prod.estado = fecha
                    prod.save()
                else:
                    pass




            response = JsonResponse({'fl':fl})
            return HttpResponse(response.content)
    except Exception as e:
        print ("OCURRIO UN SUPER ERROR Y NO SE PORQUE PERO AQUI ESTA EL MENSAJE DE ERROR")
        print (e.message)
