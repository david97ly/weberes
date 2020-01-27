# encoding=utf-8
from django import forms
from eres.models import *
import sys
# sys.setdefaultencoding() does not exist, here!
#reload(sys)  # Reload does the trick!
#sys.setdefaultencoding('UTF8')

class loginForm(forms.Form):
    username = forms.CharField( max_length = 30, widget = forms.TextInput( attrs ={
    'type': 'text',
    'name' : 'username',
    'required' : 'True',
    'id': 'nombre',
    'class' : 'codi',
    'placeholder':'Usuario',
    'onkeypress':'javascript: return ValidarNumero(event,this)'
    }) )

    password = forms.CharField( max_length = 30, widget = forms.TextInput( attrs = {
    'type' : 'password',
    'id' : 'pass',
    'name' : 'password',
    'required' : 'True',
    'class' : 'codi',
    'placeholder':'contraseña',
    'onkeypress':'javascript: return ValidarNumero(event,this)'
    } ) )





    def clean(self):


        s = self.cleaned_data['username']
        s =  s.strip()

        p = self.cleaned_data['password']
        p = p.strip()

        user_exist = User.objects.filter(username = s)

        if not user_exist:
            self.add_error('username','El usuario no existe \n asegurese de no tener espacios a los lados!')
        else:
            user = User.objects.get(username = s)
            if not user.check_password(p):
                self.add_error('password','La contraseña es incorrecta')


class UserCreateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ( 'username', 'email', 'password')
        widgets = {
           'username' : forms.TextInput( attrs = {    'type': 'text',
               'name' : 'username',
               'required' : 'True',
                'placeholder':' (ejemplo: david45)',
               'id': 'nombre',
               'value' : '',
               'class': 'codi',
               'onkeypress':'javascript: return ValidarNumero(event,this)'} ),

             'email' : forms.TextInput(attrs = {
                     'type': 'email',
                     'name' : 'username',
                     'required' : 'True',
                     'id': 'correo',
                     'value' : '',
                     'class': 'codi',
                     'placeholder':'ejemplo@gmail.com',
                     'onkeypress':'javascript: return ValidarNumero(event,this)'
             }),

              'password' : forms.TextInput(attrs = {
                  'type' : 'password',
                  'id' : 'p1',
                  'name' : 'password',
                  'required' : 'True',
                  'value' : '',
                  'class': 'codi',
                  'placeholder': 'Contraseña',
                  'onkeypress':'javascript: return ValidarNumero(event,this)'
              }),



        }

class CodigoForm(forms.ModelForm):
    class Meta:
        model = Codigo
        exclude = ('user',)
        widgets = {
           'codigo' : forms.TextInput( attrs = {'name' : 'codigo',
           'required' : 'True',
           'id': 'nombres',
           'class': 'codi',
           'value' : '',
           'placeholder': 'Ejemplo:ahb7dcr569 '
             } ),

        }

class DestacamentoForm(forms.ModelForm):
    class Meta:
        model = Destacamento
        exclude = ("user","direccion_GPS",)
        widgets = {
            'nombre' : forms.TextInput( attrs = {'name' : 'nombre',
            'required' : 'True',
            'id': 'nombre',
            'class': 'entrada',
            'value' : '',
            'placeholder': 'Nombre'
              } ),

            'codigo' : forms.TextInput( attrs = {'name' : 'codigo',
            'required' : 'True',
            'id': 'codigo',
            'class': 'entrada',
            'value' : '',
            'placeholder': 'Codigo de destacamento'
              } ),

            'iglesia' : forms.TextInput( attrs = {'name' : 'Iglesia',
            'required' : 'True',
            'id': 'iglesia',
            'class': 'entrada',
            'value' : '',
            'placeholder': 'Iglesia'
              } ),

            'pastor' : forms.TextInput( attrs = {'name' : 'pastor',
            'required' : 'True',
            'id': 'pastor',
            'class': 'entrada',
            'value' : '',
            'placeholder': 'Pastor'
              } ),

            'direccion' : forms.TextInput( attrs = {'name' : 'direccion',
            'required' : 'True',
            'id': 'direccion',
            'class': 'entrada',
            'value' : '',
            'placeholder': 'Dirección'
              } ),

            'zona' : forms.Select( attrs = {'name' : 'mes',
            'required' : 'True',
            'id': 'mes',
              } ),


        }


class PerfilForm(forms.ModelForm):
    class Meta:
        model = Perfil
        exclude = ("departamento","user","activo",'destacamento','permiso','codigo',"direccion_GPS",'year','mes','dia','sexo',)
        widgets = {
            'primer_nombre' : forms.TextInput( attrs = {'name' : 'nombrep',
            'required' : 'True',
            'id': 'nombre1',
            'class': 'entrada',
            'value' : '',
            'placeholder': 'Primer Nombre'
              } ),

            'segundo_nombre' : forms.TextInput( attrs = {'name' : 'nombres',
            'id': 'nombre2',
            'class': 'entrada',
            'value' : '',
            'placeholder': 'Segundo Nombre'
              } ),

            'primer_apellido' : forms.TextInput( attrs = {'name' : 'apellidop',
            'required' : 'True',
            'id': 'ape1',
            'class': 'entrada',
            'value' : '',
            'placeholder': 'Primer Apellido'
              } ),

            'segundo_apellido' : forms.TextInput( attrs = {'name' : 'apellidos',
            'id': 'ape2',
            'class': 'entrada',
            'value' : '',
            'placeholder': 'Segundo Apellido'
              } ),

            'telefono' : forms.TextInput( attrs = {'name' : 'telefono',
            'id': 'telefono',
            'class': 'entrada',
            'value' : '',
            'placeholder': 'Telefono'
              } ),

            'direccion' : forms.TextInput( attrs = {'name' : 'direccion',
            'id': 'direccion',
            'class': 'entrada',
            'value' : '',
            'placeholder': 'Direccion'
              } ),

             'foto' : forms.ClearableFileInput( attrs = { 'class': 'mybutton perusuario',
            'style' : 'cursor:pointer;'
             } ),


        }

class PermisoForm(forms.ModelForm):
    class Meta:
        model = Perfil
        exclude = ("departamento","user","activo",'destacamento','codigo',"direccion_GPS",'year','mes','dia','sexo',)
        widgets = {
            'primer_nombre' : forms.TextInput( attrs = {'name' : 'nombrep',
            'required' : 'True',
            'id': 'nombre1',
            'class': 'entrada',
            'value' : '',
            'placeholder': 'Primer Nombre'
              } ),

            'segundo_nombre' : forms.TextInput( attrs = {'name' : 'nombres',
            'id': 'nombre2',
            'class': 'entrada',
            'value' : '',
            'placeholder': 'Segundo Nombre'
              } ),

            'primer_apellido' : forms.TextInput( attrs = {'name' : 'apellidop',
            'required' : 'True',
            'id': 'ape1',
            'class': 'entrada',
            'value' : '',
            'placeholder': 'Primer Apellido'
              } ),

            'segundo_apellido' : forms.TextInput( attrs = {'name' : 'apellidos',
            'id': 'ape2',
            'class': 'entrada',
            'value' : '',
            'placeholder': 'Segundo Apellido'
              } ),

            'telefono' : forms.TextInput( attrs = {'name' : 'telefono',
            'id': 'telefono',
            'class': 'entrada',
            'value' : '',
            'placeholder': 'Telefono'
              } ),

            'direccion' : forms.TextInput( attrs = {'name' : 'direccion',
            'id': 'direccion',
            'class': 'entrada',
            'value' : '',
            'placeholder': 'Direccion'
              } ),

             'foto' : forms.ClearableFileInput( attrs = { 'class': 'mybutton perusuario',
            'style' : 'cursor:pointer;'
             } ),

            'permiso' : forms.Select( attrs = {'name' : 'permi',
            'required' : 'True',
            'id': 'permi',
            'style':'width: 100%;font-size:16px;margin-bottom: 10px ;',
              } ),


        }


class PublicacionForm(forms.ModelForm):
    class Meta:
        model = Publicacion
        exclude = ("user",'fecha','tiempo','fechahora','titulo',)
        widgets = {
            'descripcion' : forms.Textarea( attrs = {
            'name' : 'public',
            'id': 'inputpubli1',
            'placeholder': 'Escriba su publicación...'
              } ),


             'foto' : forms.ClearableFileInput( attrs = { 
             'id': 'subir-imagen',
             'style': 'opacity:0;',
             } ),


        }
