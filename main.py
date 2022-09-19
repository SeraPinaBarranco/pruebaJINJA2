from cgi import test
from jinja2 import Environment, FileSystemLoader #importaciones 

from model import test as t


variable = "HOLA MUNDO!!"

fileloader = FileSystemLoader("templates") #variable que almacena la carpeta de la plantilla

env = Environment(loader=fileloader) #variable que almacena el medio del template

#Obtener personal
pers = t.personal()

#Obtener el listado de plantilla
#v = t.situacion()
v = t.dias_situacion()

#Obtener los policias segun turno AP, M, T...


#print(v)

#obtiene el template y con "render" le dan las variables
rendered = env.get_template("mytemplate.html").render(personal=pers,  titulo="Estadillo")


#Escribir el resultado a un archivo del sistema de archivos
filename= "index.html"

#crea el archivo de salida
#with open(f"E:/{filename}","w") as f:
with open(f"./site/{filename}","w") as f:
    f.write(rendered)

