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

proEjec=len(tup2)-1 #cual programa se encuentra en ejecución  

print(ruta2)

"""
for tp in tup:
    nombre=tp.archivo
    ruta = str(nombre)
"""

class ejecucion:
    f = open("media/" + ruta2[proEjec], "r")
    myfile = File(f)
    print(myfile)
    leer = myfile.readlines() #para leer linea a linea #print(leer)
    f.close()
    myfile.close()
    #estructuras de datos necesarias (se contempla leer[] y ruta2[]=>que es la lista de programas(los nombres)).
    memoria =[]
    variables =[]
    posMemVar=[]
    etiquetas =[]
    memoria.append(0) # memoria en la primera posición será el acumudador (variable requerida en el ch máquina)
    
    ###############################################################################
    # necesasario para quitar el \n que se genera en algunos archivos .ch
    contadorSalto=0 # contador de salto de linea
    i=0
    contraS=""
    for i in range(len(leer)):
        contraS = leer[i] # variable para verificar si hay un salto de linea
        if contraS == str('\n'):
            contadorSalto +=1
    j=0
    for j in range(contadorSalto):
        leer.remove(str('\n'))
    ################################################################################

    #aquí se llena la memoria con el "kernel"
    i=0
    for i in range(kernel):
        memoria.append("***kernel ch***")
    cantmemoria -= kernel 

    #aquí se agregan las instrucciones a la memoria 
    for i in range(len(leer)):
        memoria.append(leer[i].rstrip())
    cantmemoria -= len(leer)
    print(cantmemoria, 'cantidad de disponible')
    #print(memoria)


    #metodo para agregar la variable a una lista con su id corresponidiente

    def varConIdProg(self, idProg, nombVar, posMemoria): # idprog > id  del programa y nombre de la variable 
        self.posMemVar.append(posMemoria) # posMemVar es global
        self.variables.append(str(idProg) + "-"+ nombVar)
        pass


    # metodos para ejecutar cada operando del arhivo .ch 
    
    def eNueva(self, linea):
        if(len(linea)==4) :
            memoria.append(linea[3])
            self.varConIdProg(proEjec, linea[1],len(memoria))
            
        elif (len(linea)==3):
            if linea[2] == 'I':
                memoria.append(0)
                self.varConIdProg(proEjec, linea[1], len(memoria))
                
            elif linea[2] == 'R':
                memoria.append(0.0)
                self.varConIdProg(proEjec, linea[1], len(memoria))

            elif linea[2] == 'L':
                memoria.append(0)
                self.varConIdProg(proEjec, linea[1], len(memoria))
            else:
                memoria.append('')
                self.varConIdProg(proEjec, linea[1], len(memoria))
        else:
            print('no se agregó nada nuevo')
    #fin funcion sNueva
        pass