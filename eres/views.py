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

    
    template = 'landing2.html'
    varible = "Exploradores"


    context = {'variable':varible}

    return render(request,template,context)

@login_required(login_url='login')
def errorcodigo(request):
    try:
        variable = 0
        context = {'variable':variable}
        template = "errorcodigo.html"
        return render(request,template,context)
    except Exception as e:
        pass


@login_required(login_url='login')
def exploblog(request):
    try:
        us  = User.objects.get(pk = request.user.id)
        context = {}
        if request.POST:
            form = PublicacionForm(request.POST,request.FILES)
            if form.is_valid():
                print("PASE POR EL FORMUALRIO")
                fo = form.save(commit=False)
                fo.user = us

                if fo.descripcion == None and fo.foto == None:
                    print("Significa que no tiene nada")
                else:
                    fo.save()
                    

   

        try:
            even = Publicacion.objects.all().order_by("-id")
            
            class event():
                id = 0
                user = ""
                fecha = ""
                tiempo = ""
                fechahora = ""
                descripcion = ""
                comentarios = ""
                favoritos = ""
                foto = ""
                comentarios = []
            
            eve = []

            for e in even:
                eventos = event()
                eventos.id = e.id
                eventos.user = e.user
                eventos.fecha = e.fecha
                eventos.tiempo = e.tiempo
                eventos.fechahora = e.fechahora
                eventos.descripcion = e.descripcion
                eventos.comentarios = e.comentarios
                eventos.favoritos = e.favoritos
                eventos.foto = e.foto

                try:
                    print("Esta es la publicacion]: " + str(e.id))
                    com = Comentario.objects.filter(publicacion=e).order_by("id")
                    print("Estos son los comentarios")
                    print(com)
                    eventos.comentarios = com

                    eve.append(eventos)
                except Exception as e:
                    print("Esta publicacion no tiene comentarios o tiene este error: " + str(e) )
                    pass


            context['eve'] = eve
            print(eve)
        except Exception as identifier:
            print("Est es el error: " + str(identifier))
            form = PublicacionForm()
            context['form'] = form

        else:
            form = PublicacionForm()
            context['form'] = form

        template = "landing1.html"
        return render(request,template,context)
    except Exception as e:
        print("Este es el error: "+ str(e))

@login_required(login_url='login')
def utilierrorcodigo(request):
    try:
        variable = 0
        context = {'variable':variable}
        template = "errorcodigo1.html"
        return render(request,template,context)
    except Exception as e:
        print("Aqui paso algo: "+ str(e))
        pass

@login_required(login_url='login')
def codigo(request):
    try:

        us  = User.objects.get(pk = request.user.id)

        try:

            per = Perfil.objects.get(user = us)

            if per:
                return redirect("/perfil")
            else:
                pass
        except Exception as e:
            print("que paso en este error: " + str(e))


        if request.POST:
            form = CodigoForm(request.POST,instance = us)
            if form.is_valid():
              
                try:
                    cod = form.cleaned_data['codigo']#capturo el codigo

                    try:
                        c = Codigo.objects.get(codigo = cod) #verifico si ese codigo ya este en el sistema
                        if c:
                            print("ESTE PERFIL ESTA SIENDO UTILIZADO")
                            return redirect("/utilierrorcodigo") # si esta lo mando a la pagina de error
                    except Exception as e:
                        pass

                    try:
                        per = Perfil.objects.get(codigo = cod)
                        print("Este es el usuario: " + str(us))
                        print("Este es el perfil: " + str(per))

                        print("Termino de Guardar")

                    except Exception as e:
                        print("ERROR PARA EL CODIGO: " + str(e))
                        return redirect("/errorcodigo")
                    else:
                        per.user = us
                        us.foto = per.foto
                        us.save()
                        per.save()

                        codn = Codigo()
                        codn.codigo = cod
                        codn.user = us
                        codn.save()
                        
                       # form.save()

                        return redirect("perfil")
                        print("lo guarde el CODIGO")


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
            nombre = ""
            if per.primer_nombre != None:
                nombre += str(per.primer_nombre)
            if per.segundo_nombre != None:
                nombre += " " + str(per.segundo_nombre)
            if per.primer_apellido != None:
                nombre += " " + str(per.primer_apellido)
            if per.segundo_apellido != None:
                nombre += " " + str(per.segundo_apellido)
            print("Este es el nombre")
            print(nombre)
            edad = calculedad(per.dia,per.mes,per.year)
            print(edad)
            email = us.email
            context = {'email':email,'per':per,'nombre':nombre,'edad':edad}
            template ="profile.html"
            print("apunto de llegar a profiles")
            return render(request,template,context)
    except Exception as e:
        print (e)
        return redirect("home")

@login_required(login_url='login')
def infoperfil(request,idperfil):
    try:
        per = Perfil.objects.get(pk = idperfil)
        email = 0
        context = {}
        try:
            us = User.objects.get(pk = per.user.id)
            email = us.email
            context['email'] = email

        except Exception as e:
            print("Esto es lo que paso:  " + str(e))
            

        nombre = ""
        if per.primer_nombre != None:
             nombre += str(per.primer_nombre)
        if per.segundo_nombre != None:
            nombre += " " + str(per.segundo_nombre)
        if per.primer_apellido != None:
            nombre += " " + str(per.primer_apellido)
        if per.segundo_apellido != None:
            nombre += " " + str(per.segundo_apellido)
        print("Este es el nombre")
        print(nombre)
        edad = calculedad(per.dia,per.mes,per.year)
        print(edad)
        
        
        template ="profile.html"

        context['edad'] = edad
        context['per'] = per
        context['nombre'] = nombre

        print("apunto de llegar a profiles")
        return render(request,template,context)
    except Exception as e:
        print("Este fue el error en ver el perfil: "+ str (e))


@login_required(login_url='login')
def destacamento(request):
    try:
        us = User.objects.get(pk = request.user.id)
        cod = Codigo.objects.get(user=us)
        print ("esto tiene codigo " + str(cod.codigo))
        if cod.codigo == None:
            return redirect("codigo")
        else:
            try:
                perfi = Perfil.objects.get(user = us)

                permiso = Permisos.objects.get(perfil=perfi)
                print("ESTE ES EL PERMISO: " + str(permiso.cargos.nivel))
                if permiso.cargos.nivel <= 2:
                    print("me voy a ver las zonas")
                    return redirect("zonas")
                elif permiso.cargos.nivel == 5:
                    print("me voy a ver el destacamento")
                    return redirect("admindestacamento")
                else:
                    print("Si tienes acceso, felicidades")
                    return redirect("perfil")

            except Exception as e:
                print("No podemos darle acceso, porque no lo tiene: " + str(e))
                return redirect("home")

            context = {'us':us}
            template ="crear-destacamento.html"
            print("apunto de llegar a profiles")

            return render(request,template,context)
    except Exception as e:
        print (e)

@login_required(login_url='login')
def inscripcion(request,iddesta):
    try:
        print("Entre a inscripcion")
        us = User.objects.get(pk = request.user.id)
        print("El usuario es: " + str(us))
        cod = Codigo.objects.get(user=us)
        print ("esto tiene codigo " + str(cod.codigo))
        if cod.codigo == None:
            return redirect("codigo")
        else:
            try:
                perfi = Perfil.objects.get(user = us)

                permiso = Permisos.objects.get(perfil=perfi)

                if not (permiso.cargos.nivel <= 5):
                    return redirect("home")
                else:
                    print("Si tienes acceso, felicidades")

            except Exception as e:
                print("No podemos darle acceso, porque no lo tiene: " + str(e))
                return redirect("home")

            try:
                destacamento = Destacamento.objects.get(pk = iddesta)
                navegantes = Perfil.objects.filter(destacamento = destacamento,departamento='Navegantes').count()
                pioneros = Perfil.objects.filter(destacamento = destacamento,departamento='Pioneros').count()
                seguidores = Perfil.objects.filter(destacamento = destacamento,departamento='Seguidores de la senda').count()
                exploradores = Perfil.objects.filter(destacamento = destacamento,departamento='Exploradores').count()
                lideres = Perfil.objects.filter(destacamento = destacamento,departamento='Lideres').count()
                tlideres = lideres * 3
                Lider = Perfil.objects.filter(destacamento = destacamento,departamento='Lideres')

                lisexplo = []
                class Exp():
                    id = 0
                    nombre = ""
                  
                print ("atnes de llegar a la carga a ala lista")
                for ex in Lider:
                    l = Exp()
                    if ex.primer_nombre != None:
                        l.nombre += ex.primer_nombre

                    if ex.segundo_nombre != None:
                        l.nombre += str(" ") + str(ex.segundo_nombre)

                    if ex.primer_apellido != None:
                        l.nombre += str(" ") + str(ex.primer_apellido)

                    if ex.segundo_apellido != None:
                        l.nombre += str(" ") + str(ex.segundo_apellido)

                    lisexplo.append(l)

            except Exception as identifier:
                print("Ocurrio un error razon: " + str(identifier))
                raise

           
            

            context = {'us':us,'destacamento':destacamento,'navegantes':navegantes,'pioneros':pioneros,'seguidores':seguidores,'exploradores':exploradores,'lideres':lideres,'Lider':lisexplo,'tlideres':tlideres}
            template ="inscripcion.html"
            

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
        print("entre a admin destacamento")
        us = User.objects.get(pk = request.user.id)
        cod = Codigo.objects.get(user=us)
        explo = False
        print ("esto tiene codigo " + str(cod.codigo))
        if cod.codigo == None:
            return redirect("codigo")
        else:

            if request.POST:
                
                abuscar = request.POST['tex']
                
                try:
                    destacamento = Destacamento.objects.get(user = request.user)
                except Exception as e:
                    return redirect("/creardestacamento")
                else:
                    explo = Perfil.objects.filter(Q(primer_nombre__icontains=abuscar)
                    | Q(segundo_nombre__icontains=abuscar) | Q(primer_apellido__icontains=abuscar) 
                    | Q(segundo_apellido__icontains=abuscar) | Q(direccion__icontains=abuscar) 
                    | Q(telefono__icontains=abuscar) 
                    | Q(codigo__icontains=abuscar) 
                    | Q(departamento__icontains=abuscar),destacamento=destacamento).exclude(primer_nombre=' ').order_by('primer_nombre')

              
            else:

                try:
                    perf = Perfil.objects.get(usr = us)
                    permiso = Permisos.objects.get(perfil = perf)

                    if not (Decimal(permiso.cargo.nivel) <= Decimal(5)):
                        return redirect("perfil")
                        
                    destacamento = Destacamento.objects.get(pk = perf.destacamento.id)


                except Exception as e:
                    return redirect("/creardestacamento")
                else:
                    explo = Perfil.objects.filter(destacamento=destacamento).exclude(primer_nombre=' ').order_by('primer_nombre')

                   
            try:
                lisexplo = []
                class Exp():
                    id = 0
                    activo = 0
                    nombre = ""
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
                    l.id = ex.id
                    l.activo = ex.activo
                    l.foto = ex.foto.url
                    l.codigo = ex.codigo
                    ed = calculedad(ex.dia,ex.mes,ex.year)
                    l.edad = ed
                    print("VEAMOS LA EDAD: " + str(ed))

                    
                    if ed > 0 and ed <= 7:
                        ex.departamento = "Navegantes"
                        ex.save()
                    elif ed > 7 and ed <= 10:
                        ex.departamento = "Pioneros"
                        ex.save()
                    elif ed > 10 and ed <= 13:
                        ex.departamento = "Seguidores de la senda"
                        ex.save()
                    elif ed > 13 and ed <= 17:
                        ex.departamento = "Exploradores"
                        ex.save()
                    else:
                        ex.departamento = "Lideres"
                        ex.save()


                    lisexplo.append(l) 

            except Exception as e:
                pass


            context = {'us':us,'destacamento':destacamento,'lisexplo':lisexplo,'iddesta':destacamento.id}
            template ="lista.html"
            print("apunto de llegar a profiles")

            return render(request,template,context)
    except Exception as e:
        print ("El error al entrar al admindestacamento es: " + str(e))
        return redirect("/")





@login_required(login_url='login')
def detalledestacamento(request, iddesta):
    try:
        print("entre a admin destacamento")
        us = User.objects.get(pk = request.user.id)
        cod = Codigo.objects.get(user=us)
        explo = False
        print ("esto tiene codigo " + str(cod.codigo))
        if cod.codigo == None:
            return redirect("codigo")
        else:
            try:
                perfi = Perfil.objects.get(user = us)

                permiso = Permisos.objects.get(perfil=perfi)

                if not (permiso.cargos.nivel <= 2):
                    return redirect("home")
                else:
                    print("Si tienes acceso, felicidades")

            except Exception as e:
                print("No podemos darle acceso, porque no lo tiene: " + str(e))
                return redirect("home")


            if request.POST:
                
                abuscar = request.POST['tex']
                
                try:
                    destacamento = Destacamento.objects.get(pk=iddesta)
                except Exception as e:
                    return redirect("/creardestacamento")
                else:
                    explo = Perfil.objects.filter(Q(primer_nombre__icontains=abuscar)
                    | Q(segundo_nombre__icontains=abuscar) | Q(primer_apellido__icontains=abuscar) 
                    | Q(segundo_apellido__icontains=abuscar) | Q(direccion__icontains=abuscar) 
                    | Q(telefono__icontains=abuscar) 
                    | Q(codigo__icontains=abuscar) 
                    | Q(departamento__icontains=abuscar),destacamento=destacamento).exclude(primer_nombre=' ').order_by('primer_nombre')

              
            else:

                try:
                    destacamento = Destacamento.objects.get(pk = iddesta)
                except Exception as e:
                    return redirect("/creardestacamento")
                else:
                    explo = Perfil.objects.filter(destacamento=destacamento).exclude(primer_nombre=' ').order_by('primer_nombre')

                   
            try:
                lisexplo = []
                class Exp():
                    id = 0
                    activo = 0
                    nombre = ""
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
                    l.id = ex.id
                    l.activo = ex.activo
                    l.foto = ex.foto.url
                    l.codigo = ex.codigo
                    ed = calculedad(ex.dia,ex.mes,ex.year)
                    l.edad = ed
                    print("VEAMOS LA EDAD: " + str(ed))

                    
                    if ed > 0 and ed <= 7:
                        ex.departamento = "Navegantes"
                        ex.save()
                    elif ed > 7 and ed <= 10:
                        ex.departamento = "Pioneros"
                        ex.save()
                    elif ed > 10 and ed <= 13:
                        ex.departamento = "Seguidores de la senda"
                        ex.save()
                    elif ed > 13 and ed <= 17:
                        ex.departamento = "Exploradores"
                        ex.save()
                    else:
                        ex.departamento = "Lideres"
                        ex.save()


                    lisexplo.append(l) 

            except Exception as e:
                pass


            context = {'us':us,'destacamento':destacamento,'lisexplo':lisexplo,'iddesta':iddesta}
            template ="listazonadestacamento.html"
            print("apunto de llegar a profiles")

            return render(request,template,context)
    except Exception as e:
        print ("El error al entrar al admindestacamento es: " + str(e))
        return redirect("/")



@login_required(login_url='login')
def zonadestacamentos(request,idzona):
    try:
        print("entre a admin destacamento")
        us = User.objects.get(pk = request.user.id)
        cod = Codigo.objects.get(user=us)
        
        print ("esto tiene codigo " + str(cod.codigo))
        if cod.codigo == None:
            return redirect("codigo")
        else:
            try:
                perfi = Perfil.objects.get(user = us)

                permiso = Permisos.objects.get(perfil=perfi)
                nivel = permiso.cargos.nivel
                if not (nivel <= 2):
                    return redirect("home")
                else:
                    print("ESTA SON LAS ZONAS: "+ str(idzona) + "  -  " + str(perfi.destacamento.zona.id))
                    if nivel == 2:
                        if Decimal(idzona) != Decimal(perfi.destacamento.zona.id):
                            print("Son diferentes asi que al home")
                            return redirect("home")

                    print("Si tienes acceso, felicidades")

            except Exception as e:
                print("No podemos darle acceso, porque no lo tiene: " + str(e))
                return redirect("home")

            if request.POST:
                
                abuscar = request.POST['tex']
                
                try:
                    destacamento = Destacamento.objects.get(user = request.user)
                except Exception as e:
                    return redirect("/creardestacamento")
                else:
                    explo = Perfil.objects.filter(Q(primer_nombre__icontains=abuscar)
                    | Q(segundo_nombre__icontains=abuscar) | Q(primer_apellido__icontains=abuscar) 
                    | Q(segundo_apellido__icontains=abuscar) | Q(direccion__icontains=abuscar) 
                    | Q(telefono__icontains=abuscar) 
                    | Q(codigo__icontains=abuscar) 
                    | Q(departamento__icontains=abuscar),destacamento=destacamento).exclude(primer_nombre=' ').order_by('primer_nombre')

              
            else:

                try:
                    zona = Zona.objects.get(pk = idzona)
                    destacamentos = Destacamento.objects.filter(zona = zona)
                    
                except Exception as e:
                    print("AQUI OCURRIO UN ERRO EN LA ZONA: " + str(e))
                    return redirect("home")
               
                   
                   


            context = {'destacamentos':destacamentos,'zona':zona,}
            template ="listazona.html"
            print("apunto de llegar a profiles")

            return render(request,template,context)
    except Exception as e:
        print ("El error al entrar al admindestacamento es: " + str(e))
        raise
        #return redirect("/")


@login_required(login_url='login')
def zonas(request):
    try:
        print("entre a admin destacamento")
        us = User.objects.get(pk = request.user.id)
        cod = Codigo.objects.get(user=us)
        
        print ("esto tiene codigo " + str(cod.codigo))
        if cod.codigo == None:
            return redirect("codigo")
        else:
            try:
                perfi = Perfil.objects.get(user = us)

                permiso = Permisos.objects.get(perfil=perfi)

                if not (permiso.cargos.nivel <= 2):
                    return redirect("home")
                else:
                    print("Si tienes acceso, felicidades")
            except Exception as e:
                print("Lo siento pero no tienes acceso: " + str(e))
                return redirect("home")

            if request.POST:
                
                abuscar = request.POST['tex']
                
                try:
                    destacamento = Destacamento.objects.get(user = request.user)
                except Exception as e:
                    return redirect("/creardestacamento")
                else:
                    explo = Perfil.objects.filter(Q(primer_nombre__icontains=abuscar)
                    | Q(segundo_nombre__icontains=abuscar) | Q(primer_apellido__icontains=abuscar) 
                    | Q(segundo_apellido__icontains=abuscar) | Q(direccion__icontains=abuscar) 
                    | Q(telefono__icontains=abuscar) 
                    | Q(codigo__icontains=abuscar) 
                    | Q(departamento__icontains=abuscar),destacamento=destacamento).exclude(primer_nombre=' ').order_by('primer_nombre')

              
            else:

                try:
                    lista = []
                    class ZonaClass():
                        idzona = 0
                        nombre = ""
                        desta = 0

                    zonas = Zona.objects.all().order_by("numero")
                    print("Estas son las zonas: " + str(zonas))
                    for z in zonas:
                        zon = ZonaClass()
                        zon.nombre = z.nombre
                        zon.idzona = z.id
                        try:
                            zon.desta = Destacamento.objects.filter(zona = z).count()
                            lista.append(zon)
                        except Exception as e:
                            print("Esta zona no tiene destacamentos: "+ str(e))
                            pass

                    
                except Exception as e:
                    print("AQUI OCURRIO UN ERRO EN LA ZONA: " + str(e))
                    return redirect("home")
               
                   
                   


            context = {'lista': lista}
            template ="zonas.html"
            print("apunto de llegar a profiles")

            return render(request,template,context)
    except Exception as e:
        print ("El error al entrar al admindestacamento es: " + str(e))
        raise
        #return redirect("/")


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


                perfiles = Perfil.objects.all()
                supercod = ""
                fl = True

                while(fl==True):
                    ncodigo = generarnumeros(str(str(siglasz) + str(des) + str(codigo)))
                    supercod  = str(siglasz) + str(des) + str(desta.codigo) + str(codigo) + str(ncodigo)
                    fl = False
                    for p in perfiles:
                        if str(p.codigo).strip() == str(supercod).strip():
                            fl = True



                fo.codigo = supercod

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


@login_required(login_url='login')
def editarexplorador(request,iddesta,idexplo):
    try:
        desta = Destacamento.objects.get(pk=iddesta)
        perf = Perfil.objects.get(pk=idexplo)

    except Exception as e:
        print(e)
        return redirect("home")


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


                perfiles = Perfil.objects.all()
                supercod = ""
                fl = True

                while(fl==True):
                    ncodigo = generarnumeros(str(str(siglasz) + str(des) + str(codigo)))
                    supercod  = str(siglasz) + str(des) + str(desta.codigo) + str(codigo) + str(ncodigo)
                    fl = False
                    for p in perfiles:
                        if str(p.codigo).strip() == str(supercod).strip():
                            fl = True



                fo.codigo = supercod

                fo.save()
                return redirect("/admindestacamento")
        else:
            tp = ''
            n = 1910
            form = PerfilForm(instance=perf)
            template = 'Sign_Up.html'

            context = {'form':form,'n':n,'tp':tp,'perf':perf,'idexplo': idexplo,'iddesta':iddesta}

        return render(request,template,context)
    except Exception as e:
        raise




@login_required(login_url='login')
def editardestacamento(request,iddesta):
    try:
        desta = Destacamento.objects.get(pk=iddesta)
        

    except Exception as e:
        print(e)
        return redirect("home")


    try:
        if request.POST:
            form = DestacamentoForm(request.POST,request.FILES,instance=desta)
            if form.is_valid():

                form.save()
                return redirect("/admindestacamento")
        else:
           
            form = DestacamentoForm(instance=desta)
            template = "registrar-destacamento.html"

            context = {'form':form}

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



class Block(TemplateView):
    print ("SIQUIERA ENTRE AQUI AL AJAX")
    try:
        def get(self,request,*args,**kwargs):
           
        
            id = request.GET['idexp']
            print("El id es: " + str(id))

            per = Perfil.objects.get(pk = id)

            print("El perfil es: " + str(per.primer_nombre))
            fl = False

            if per.activo == True:
                per.activo = False
                per.save()
                fl =  False
            else:
                per.activo = True
                per.save()
                fl = True

            print("FL es: " + str(fl))
          

         


            response = JsonResponse({'fl':fl, 'id':id})
            return HttpResponse(response.content)
    except Exception as e:
        print ("OCURRIO UN SUPER ERROR Y NO SE PORQUE PERO AQUI ESTA EL MENSAJE DE ERROR")
        print (e.message)



class MensajeEnviar(TemplateView):
    try:
        def get(self,request,*args,**kwargs):
            texto = request.GET['texto']
            publicacion = request.GET['p']

         
            print (texto)
            print (publicacion)
        


            try:
                
                us = User.objects.get(username = request.user)
                pub = Publicacion.objects.get(pk = publicacion)
            except Exception as e:
                print ("lO SIENTO NO HAY CHAT : " + str(e.message))
            else:
                try:
                   com = Comentario()
                   com.user = us
                   com.publicacion = pub
                   com.texto = texto
                   com.save()

                   fecha = com.fecha.strftime('%d %b')
                   hora = com.tiempo.strftime("%X %p")

                except Exception as e:
                    print ("UPS!! OCURRIO ALGO : " + str(e))
                else:
                    print ("TODO SALIO BIEN")
            response = JsonResponse({'texto':texto,'fecha':fecha,'hora':hora})
            return HttpResponse(response.content)

    except Exception as e:
        print ("La regue en algo vamos en que: " + str(e))

