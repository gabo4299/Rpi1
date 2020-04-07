#El indexraspeberry es el  uso en la rpi lo unico que agrega o modifica es el def encender 
import RPi.GPIO as GPIO #Librería para controlar GPIO
GPIO.setmode(GPIO.BCM) #Simplemente nos sirve para usar números de pin de placa y no del procesador
GPIO.setwarnings(False)
foco = 21 #Variable donde ponemos el pin que usaremos para el LED
lecturaarriba=20
lecturaabajo=26
cortinapin=16


GPIO.setup(led, GPIO.OUT)
GPIO.setup(lecturaarriba, GPIO.IN,GPIO.PUD_UP)
GPIO.setup(lecturaabajo, GPIO.IN,GPIO.PUD_UP)
s.GPIO.PWM(cortinapin,50)
s.start(0.0)
from flask import Flask, render_template , request
from flask_socketio import SocketIO , send  , emit
import threading 
import time   
import subprocess
from eventlet import tpool
#Ayuda estado anterior
app = Flask(__name__)
cont=1

app.config['SECRET_KEY']='secret'
socketio=SocketIO(app)
#falta en (app,async mode='threading") 
#nota sin el async mode no se puede parar el programa con cntrol c , pero si es en tiempo real !

@app.route('/')
def home():
    
    return render_template('home2.html')
encendiendo='1'
@app.route('/cerrar')
def caca():
    global encendiendo
    e='0'
    encendiendo=e
    return ("cerrado")
@app.route('/abrir')
def caca2():
    global encendiendo
    e='1'
    encendiendo=e
    return ("abierto")


@socketio.on('luz')
def hacer(accion):

    global encendiendo
    if accion=='Encender':
        
        GPIO.output(foco,1)
        luza=open('estado_luz.txt','w')
        luza.write('Encendido')
        luza.close()
        estado='Encendido'
        emit('id','Encendido',broadcast=True)
        encendiendo='1'
        
    if accion=='Apagar':
        GPIO.output(foco,0)
        luza=open('estado_luz.txt','w')
        luza.write('Apagado')
        estado='Apagado'
        luza.close()
        emit('id','Apagado',broadcast=True)
        
        encendiendo='0'
        
    else:
         luza=open('estado_luz.txt' , 'r')
         estado=luza.read()
         luza.close()
         print(estado)
         emit('id',estado,broadcast=True)
   
''' var=accion
    tpool.execute(encenderLuz,'1',var)'''
    # o tambien
#    socketio.start_background_task(target=encenderLuz, ('1',var))
   
'''hiloluz=threading.Thread(target=encenderLuz('1','var'))
    hiloluz.start()
    
    hiloluz.join()'''
   

def encenderLuz(numero, estado):
    global encendiendo
    while estado=='Encender':
        if encendiendo=='1':
            print(numero + " " + estado+ " " + encendiendo)
            time.sleep(0.2)
        else:
            break
    else:
        while estado=='Apagar':
            if encendiendo=='1':
                print(estado + " " + numero)
                time.sleep(0.2)
            else:
                break

leeyendo='1'

def abrirtextocortina():
      cor=open('estado_cortina.txt','r')
      estado=cor.read()
      cor.close()
      return estado


@socketio.on('parar')
def parar():
    global leeyendo
    leeyendo='0'


@socketio.on('cortina')
def hacercortina(click,accionCortina):
    global leeyendo
    if(accionCortina!='X'):
        if click=='SI':
            leeyendo='1'
            #si es si empeiza a leer , hasta que se cierre puedes usar el leendo para ayudarte, y paralelamente vas a ir subiendo o bajando o la funcion bajando totalmetne
            print("si"+accionCortina)
            estado=abrirtextocortina()
            if accionCortina=='x':
                time.sleep(0.1)
                emit('id2',(estado,'SI'),broadcast=True)
                tpool.execute(leersensores,'1')
                
            
            # la lectura puedews usar una funcion y usar un retur con el dato en estado enves de read y como se cierra con el leyendo podria funcionar intentar !! 
            if accionCortina=='subiendo':
                
                estado=abrirtextocortina()
                if estado!='Abierto':
                    s.ChangeDutyCycle(4.5)
                    time.sleep(0.2)
                    print ('subiendo poco  a poco')
                    s.ChangeDutyCycle(0)
                    
                    

            if accionCortina=='bajando':
                estado=abrirtextocortina()
                if estado!='Cerrado':           
                    
                    s.ChangeDutyCycle(8.5)
                    time.sleep(0.2)
                    print("bajando poco a poco")
                    s.ChangeDutyCycle(0)

            if accionCortina=='abriendo':
                while True:
                    estado=abrirtextocortina()
                    if (estado!="Abierto" and accionCortina=="abriendo"):
                      s.ChangeDutyCycle(4.5)  
                      time.sleep(0.01)
                      print("Abriendo totalemtne  :" + accionCortina )
                    else:
                        s.ChangeDutyCycle(0.0)
                        time.sleep(0.01)
                        break
                
            if accionCortina=='cerrando':
                print('cerrando completamente')
                while True:
                    estado=abrirtextocortina()
                    if (estado!="Cerrado" and accionCortina=="cerrando"):           
                      s.ChangeDutyCycle(8.5)  
                      time.sleep(0.01)
                     print("cerrando totalemtne  :" + accionCortina )
                    else:
                        s.ChangeDutyCycle(0.0)  
                      time.sleep(0.01)
                        break

        else:
            if click=='NO':
                leeyendo='0'
                time.sleep(0.1)
                print('no')
                cor=open('estado_cortina.txt','r')
                estado=cor.read()
                cor.close()
                print(estado)
                emit('id2',(estado,'NO'),broadcast=True)
            if click=='SO':

                time.sleep(0.1)
                print('no sin parar ciclo')
                cor=open('estado_cortina.txt','r')
                estado=cor.read()
                cor.close()
                print(estado)
                emit('id2',(estado,'NO'),broadcast=True)
        
            #emite el mensaje con la lectura del estado
def leersensores(id):
    global leeyendo
    tocasabajo=11
    tocasarriba=11

    while (leeyendo=='1'):
        if(leeyendo=='1'):
            tocasabajo = GPIO.input(lecturaabajo)
            tocasarriba= GPIO.input(lecturaarriba)
            if tocasarriba==1:
                cor=open('estado_cortina.txt','w')
                cor.write('Abierto')
                cor.close
            if tocasabajo==1:
                cor=open('estado_cortina.txt','w')
                cor.write('Cerrado')
                cor.close
            if tocasarriba==0 & tocasabajo==0:
                cor=open('estado_cortina.txt','w')
                cor.write('Semi')
                cor.close

            print('leyendo'+id)
            time.sleep(0.1)
        else:
            break
    


if __name__ == '__main__':
    
    #app.run(debug=True , host= '0.0.0.0', threaded=True)
    socketio.run(app,debug=True)
 