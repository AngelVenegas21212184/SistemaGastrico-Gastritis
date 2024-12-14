"""
Proyecto final: Sistema Gastrico


Departamento de Ingeniería Eléctrica y Electrónica, Ingeniería Biomédica
Tecnológico Nacional de México [TecNM - Tijuana]
Blvd. Alberto Limón Padilla s/n, C.P. 22454, Tijuana, B.C., México

Nombre del alumno: 
    Armenta Contreras Odin Enrique
    Paniagua Fernandez Jaime Jhoelly
    Venegas Ameca Angel Ismael 
Número de control: 
    21212140
    21212171
    21212184
Correo institucional: 
    l21212140@tectijuana.edu.mx
    l21212171@tectijuana.edu.mx
    l21212184@tectijuana.edu.mx

Asignatura: Modelado de Sistemas Fisiológicos
Docente: Dr. Paul Antonio Valle Trujillo; paul.valle@tectijuana.edu.mx
"""
# Instalar librerias en consola
#!pip install control
#!pip install slycot

# Librerías para cálculo numérico y generación de gráficas
import numpy as np
import matplotlib.pyplot as plt
import control as ctrl
import math as m

# Datos de la simulación
x0, t0, tF, dt, w, h=0, 0, 10, 1E-3, 8, 5
N = round((tF-t0)/dt)+1
t = np.linspace(t0,tF,N)
u = np.sin(m.pi/2*t) #Funcion sinusoidal, 1.5708 rad/s = 250 mHz

#Función de transferencia: Individuo Saludable (Control)
R= 100
L=3.3E-3
C1=1
C2=1
num = [R*C1]
den = [((L*R*C1*C2)) ,(L*C2+L*C1),(R*C2+R*C1)]
sys = ctrl.tf(num,den)
print('Individuo sano (control):')
print(sys)

#Función de transferencia: Individuo Enfermo (Caso)
RA= 400
C1A=0.75
C2A=0.2
num = [RA*C1A]
den = [(L*RA*C1A*C2A) ,+((L*C2A)+(L*C1A)),+((RA*C2A)+(RA*C1A))]
sysE = ctrl.tf(num,den)
print('Individuo enfermo (caso):')
print(sysE)

# Componentes del controlador
Rr = 209.97E3
Re = 181.9
Cr = 0.1E-6
Ce= 0.25649E-6
numPID = [Rr*Re*Cr*Ce,Re*Ce+Rr*Cr,1]
denPID = [Re*Cr, 0]
PID = ctrl.tf(numPID, denPID)
print(PID) 

#Sistema de control de tratamiento
X = ctrl.series(PID,sysE)
sysPID = ctrl.feedback(X,1,sign=-1)
print('Sistema con tratamiento')
print(sysPID)

fig = plt.figure()
plt.plot(t, u, '-', color = [0.6, 0.8, 0.9], label = 'Ventrada')
ts,Vs = ctrl.forced_response(sys,t,u,x0)
plt.plot(t, Vs, '-', color = [0.9, 0.7, 0.8], label = 'V(t):Control')
ts,Ve = ctrl.forced_response(sysE,t,u,x0)
plt.plot(t,Ve, "-" ,color = [0.7, 0.9, 0.7],label = "V(t):Caso")
ts,pid = ctrl.forced_response(sysPID,t,Vs,x0)
plt.plot(t,pid,':', linewidth = 3, color = [0.9, 0.8, 0.6], label = 'V(t):Tratamiento')
plt.grid(False)

#Configuracion de limites
plt.xlim(0,10.1)
plt.xticks(np.arange(0, 10.1, 1))
plt.ylim(-1.25,1.25)
plt.yticks(np.arange(-1.25, 1.25, 0.25))
 
#Personalizacion de la grafica   
plt.title("Modelo Fisiologico del Sistema Gastrico", fontsize = 13) #Titulo de la grafica        
plt.xlabel('$t$[segundos]', fontsize = 11) #Etiqueta EjeX
plt.ylabel('$V(t)$ [Esfuerzo Gastrico]', fontsize = 11) #Etiqueta EjeY
plt.legend(bbox_to_anchor = (0.5,-0.23),loc = 'center',ncol = 4) #Caja de leyendas

fig.set_size_inches(w, h) #Configuracion de tamaño de imagen
fig.tight_layout() 
namepng = 'sistema_gastrico' + '.png'
namepdf = 'sistema_gastrico' + '.pdf'
fig.savefig(namepng, dpi = 600,bbox_inches = 'tight')
fig.savefig(namepdf, bbox_inches = 'tight')

# Respuesta del sistema en lazo abierto y en lazo cerrado
#for i in range(1,6):
#    plotsignals(u[:, i-1], sys,sysE, sysPID, signal[i-1])