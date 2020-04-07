#El indexraspeberry es el  uso en la rpi lo unico que agrega o modifica es el def encender 
'''import RPi.GPIO as GPIO #Librería para controlar GPIO
GPIO.setmode(GPIO.BCM) #Simplemente nos sirve para usar números de pin de placa y no del procesador
GPIO.setwarnings(False)
led = 21 #Variable donde ponemos el pin que usaremos para el LED
GPIO.setup(led, GPIO.OUT)'''
from flask import Flask, render_template , request
from flask_socketio import SocketIO , send  , emit
import threading 
import time   
import subprocess
import eventlet
#Ayuda estado anterior
app = Flask(__name__)

luz=open('estado_luz.txt','r')
estado_luz=luz.read()
luz.close()
m=open('ConfiguracionVentana.txt','r')
estadomotor=m.read()
m.close()


app.config['SECRET_KEY']='secret'
socketio=SocketIO(app)
print ("socket abierto", socketio)

@app.route('/')
def home(): 
    
   return render_template ('home.html',est=estado_luz,A=encender,estad=estadomotor) 

@app.route('/luz/<string:estado_luz2>')
def home1(estado_luz2):
   if (estado_luz2==("Apagado")):
      aux("Apagado")
   else:
      if (estado_luz2==("Encendido")):
        
         aux("Encendido")     
   return render_template('home.html',est=estado_luz2,A=encender,estad=estadomotor)
 
@app.route('/motor/<string:motr>')
def mot(motr):
   global estadomotor
   m=open('ConfiguracionVentana.txt','r')
   estadomotor=m.read()
   m.close()
   return render_template('home.html',est=estado_luz,A=encender,estad=estadomotor, ac=cerrarsubproceso)
    
def encender(i):
    if i=="Encendido":  
        print("Encendido ctm")
      # GPIO.output(21,0)
      # time.sleep(0.0001)
        time.sleep(0.0001)
        return(' ')
    else :
        print("Apagado")
      # GPIO.output(21,0)
      # time.sleep(0.0001)
        time.sleep(0.0001)
        return(' ')

@socketio.on('hacer')
def ciclo(ms):
   if ms=='Subir':
      print(ms)
      esc=open('ConfiguracionVentana.txt','w')
      esc.write('SI')   
      esc.close()
      subprocess.call('python '+' "input.py"  ' + 'exit()', shell=True)

@socketio.on('bajar')
def ciclo2(ms):
   if ms=='NO':
      print(ms)
      cerrarsubproceso()

def aux(s):
   global estado_luz
   estado_luz=s
   esc=open('estado_luz.txt','w')
   esc.write(s)
   esc.close() 
   print (estado_luz)
        
def cerrarsubproceso():
   esc=open('ConfiguracionVentana.txt','w')
   esc.write('NO')
def motor():
   subprocess.call('python '+' "motor.py"  ' + 'exit()', shell=True)



    
   
 
    
    
    
  
if __name__ == '__main__':
    
    #app.run(debug=True , host= '0.0.0.0', threaded=True)
    socketio.run(app,debug=True)
 




