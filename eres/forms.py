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
            self.add_error('username','El nombre de Usuario no exiiste!')
        else:
            user = User.objects.get(username = s)
            if not user.check_password(p):
                self.add_error('password','La contraseña es incorrecta')
