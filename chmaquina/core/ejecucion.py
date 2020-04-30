from django.core.files import File
from .models import EjecArchCh

ruta =""
#tup = ArchivosCh.objects.all()
tup2 = EjecArchCh.objects.all()
#aqui se agregan todos los archivos para abrir 
ruta2=[]
w=0
cantmemoria=-2
kernel=-3

for tp in tup2:
    nombre2=tp.archivo
    tempo = tp.memoria
    cantmemoria=int(tempo)
    tempo = tp.kernel
    kernel=int(tempo)
    ruta2.append(str(nombre2))
    
print(ruta2)

"""
for tp in tup:
    nombre=tp.archivo
    ruta = str(nombre)
"""

class ejecucion:
    f = open("media/" + ruta2[1], "r")
    myfile = File(f)
    print(myfile)
    leer = myfile.readlines() #para leer linea a linea #print(leer)
    f.close()
    myfile.close()
    memoria =[]
    memoria.append(0) # memoria en la primera posición será el acumudador (variable requerida en el ch máquina)
    
    #aquí se llena la memoria con el "kernel"
    for i in range(kernel):
        memoria.append("***kernel ch***")
    
    #aquí se agregan las instrucciones a la memoria 
    for i in range(len(leer)-1):
        memoria.append(leer[i].rstrip())
    print(memoria)

    # metodos para ejecutar cada operando del arhivo .ch 
    
    def eNueva(self, linea):
        
        pass