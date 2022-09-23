from cgi import test
from jinja2 import Environment, FileSystemLoader #importaciones 

from model import test as t

import os
from datetime import datetime, timedelta

#ruta
ruta = "\\datos\policia\OficinaTecnica\escudos\EscudoJPG.jpg"
rutaABS= os.path.abspath(ruta)

#FECHA DEL ESTADILLO
hoy = datetime.now()
ayer = hoy.day - 1
mes = str(hoy.month)
if( len(mes)== 1):
    mes = "0{}".format(mes)
#FECHA ACTUAL
fecha =  "{}/{}/{}".format(hoy.day,mes,hoy.year)

#BAJAS
bajas = t.bajas()


fileloader = FileSystemLoader("templates") #variable que almacena la carpeta de la plantilla

env = Environment(loader=fileloader) #variable que almacena el medio del template

#Obtener personal
pers = t.personal()

#Obtener el listado de plantilla
#v = t.situacion()
v = t.dias_situacion(fecha)

#Obtener las denuncias AYTO
ayer = hoy - timedelta(1)
mesAyer = str(ayer.month)
if( len(mesAyer)== 1):
    mesAyer = "0{}".format(mesAyer)
fechaAyer =  "{}/{}/{}".format(ayer.day,mesAyer,ayer.year)

ayto = t.denuncias_ayto(fechaAyer)
jpt = t.denuncias_JPT(fechaAyer)
cam = t.denuncias_CAM(fechaAyer)
radar = t.radar(fechaAyer)

#Obtener vehiculos que entraron en deposito
deposito = t.deposito(fechaAyer)

#Obtener tipo vehiculos que entraron en deposito
tipoVehDep = t.tipo_vehiculo_deposito(fechaAyer)

#Obtener datos REGISTRO ENTRADA
reg_ent= t.registro_entrada(fechaAyer)

#obtiene el template y con "render" le dan las variables
rendered = env.get_template("mytemplate.html").render(personal=pers, listado_personal=v, titulo="Estadillo", fecha= fecha, ruta= rutaABS, bajas = bajas, ayto=ayto, jpt=jpt,cam=cam, radar=radar, deposito=deposito, tvd= tipoVehDep, reg_ent=reg_ent)


#Escribir el resultado a un archivo del sistema de archivos
filename= "index.html"

#crea el archivo de salida
#with open(f"./site/{filename}","w") as f:
with open(f"\\\datos\\policia\\OficinaTecnica\\{filename}","w") as f:
    f.write(rendered)
    #f.write(f"D:\\{filename}","w")
    print(os.getcwd())

