# coding=utf-8
from datetime import datetime
from .models import *
from decimal import Decimal
from random import choice
import sys
# sys.setdefaultencoding() does not exist, here!


def calculedad(dia,mes,year):
    try:
        d = datetime.today()
        print ("ESTA ES LA EDAD DE LA BASE DE DATOS: dia(" + str(dia) + str(") mes(" + str(mes) + str(") Year(") + str (year) + ")"))
        anoactual = d.year
        mesactual = d.month
        diactual = d.day

        anonaci = year
        mesnaci = mes
        dinaci = dia

        if mes == 'enero':
            mesnaci = 1
        elif mes == 'febrero':
            mesnaci = 2
        elif mes == 'marzo':
            mesnaci = 3
        elif mes == 'abril':
            mesnaci = 4
        elif mes == 'mayo':
            mesnaci = 5
        elif mes == 'junio':
            mesnaci = 6
        elif mes == 'julio':
            mesnaci = 7
        elif mes == 'agosto':
            mesnaci = 8
        elif mes == 'septiembre':
            mesnaci = 9
        elif mes == 'octubre':
            mesnaci = 10
        elif mes == 'noviembre':
            mesnaci = 11
        elif mes == 'diciembre':
            mesnaci = 12
        else:
            mesnaci = 1

        edad = anoactual - anonaci
        print ("EDAD ANTES: " + str(edad))
        if mesactual > mesnaci:
            pass
            # "todavia no ha llegado al mes de nacimiento"
        else:
            # "ya llego al mes de nacimiento"
            if mesactual == mesnaci:
                # "El mes de nacimiento es igual"
                if not diactual >= dinaci:
                    edad = edad - 1
            else:
                # "No es igual al mes actual"
                if mesactual < mesnaci:
                    # "el mes de cumple es menor significa que no ha cumplido " + str(edad)
                    edad = edad - 1

        print ("EDAD DESPUES: " + str(edad))


        return edad
    except Exception as e:
        print("Ocurrio un error al calcular la edad: " + str(e))
        return 0


def reemplazar(original,reemplazo,palabra):
    try:
        newpalabra = ""
        for i in palabra:
            if i == original:
                newpalabra+=reemplazo
            else:
                newpalabra+=i

        return newpalabra
    except Exception as e:
        print ("Tampoco se puede en este metodo inventado por mi razon: " + str(e))



def crearslug(palabra):
    try:
        nuevap = ""
        for p in palabra:

            if (ord(p) >= 65 and ord(p) <= 90) or (ord(p) >= 97 and ord(p) <=122) or (ord(p) == 130 or ord(p) == 181 or ord(p) == 252 or ord(p) == 209 or ord(p) == 241 or ord(p) == 218 or ord(p) == 201 or ord(p) == 193 or ord(p) == 45 or ord(p) == 225 or ord(p) == 233 or ord(p)==237 or ord(p)==243 or ord(p)==250 or ord(p)== 220) :

                nuevap += p

        return nuevap
    except Exception as e:
        print ("Este es el error que dio: " + str(e))



def siglas(palabra):
    try:
        contador = 0
        sigla = ""
        espacio = False

        for p in palabra:
            if contador == 0:
                sigla += p
            else:
                if p == ' ':
                    espacio = True
                    sigla += palabra[contador+1]
            contador += 1

        if not espacio:
            sigla = palabra[0] + palabra[1]

        nsigla = ""

        for s in sigla:
            aux = ord(s)

            if aux >= 65 and aux <= 90:
                aux += 32
                nsigla += chr(aux)
            else:
                nsigla += chr(aux)

        sigla = nsigla

        return sigla

    except Exception as e:
        print("Ocurrio un erro razon: " + str(e))

def generarnumeros(cadena):
    try:
        num = ""

        num += str(ord(choice(cadena)))

        num += str(ord(choice(cadena)))

        num += str(ord(choice(cadena)))

        num += str(ord(choice(cadena)))

        nnum = ""
        contador = 0

        for p in num:
            if contador <=3:
                nnum += p

            contador += 1

        num = nnum

        return num

    except Exception as e:
        print("Aqui ocurrio un error razon: " + str(e))


def minus(cadena):
    try:
        nsigla = ""
        
        for s in cadena:
            aux = ord(s)

            if aux >= 65 and aux <= 90:
                aux += 32
                nsigla += chr(aux)
            else:
                nsigla += chr(aux)

        sigla = nsigla

        return sigla
    except Exception as e:
        raise
