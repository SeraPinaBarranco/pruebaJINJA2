from jinja2 import Environment, FileSystemLoader #importaciones 

variable = "HOLA MUNDO!"

fileloader = FileSystemLoader("templates") #variable que almacena la carpeta de la plantilla

env = Environment(loader=fileloader) #variable que almacena el medio del template

#obtiene el template y con "render" le dan las variables
rendered = env.get_template("mytemplate.html").render(v=variable, titulo="JINJA 2 Templates")

print(rendered)

#Escribir el resultado a un archivo del sistema de archivos
filename= "index.html"

#crea el archivo de salida
#with open(f"E:/{filename}","w") as f:
with open(f"./site/{filename}","w") as f:
    f.write(rendered)