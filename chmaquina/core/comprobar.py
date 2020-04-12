from django.core.files import File
#from io import .
from .models import ArchivosCh


#ruta=request.FILES.get('archivo')
ruta =""
tup = ArchivosCh.objects.all()
for tp in tup:
    nombre=tp.archivo
    ruta = str(nombre)
class sintax:
    #while(True):
    
    
    #ruta = "media/" + ruta
    #print(ruta) 

    f = open("media/" + ruta, "r")
    myfile = File(f)
    print(myfile)
    leer = myfile.read()
    print(leer)
    f.close()
    myfile.close()
    
    def abrirArchivo(self):
        return str(self.leer)

    
#print(sintax.abrirArchivo())