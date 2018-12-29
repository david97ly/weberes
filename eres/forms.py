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
