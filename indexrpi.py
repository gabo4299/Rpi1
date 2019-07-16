from flask import Flask, render_template , request
import threading 
import time
import RPi.GPIO as GPIO #Librería para controlar GPIO
GPIO.setmode(GPIO.BCM) #Simplemente nos sirve para usar números de pin de placa y no del procesador
GPIO.setwarnings(False)
led = 21 #Variable donde ponemos el pin que usaremos para el LED
GPIO.setup(led, GPIO.OUT)

app = Flask(__name__)
estado_luz=""
estado_luz2="h"
@app.route('/')
def home(): 
    global estado_luz
    return render_template ('home.html',est=estado_luz,A=encender)
    
def encender(i):
    global estado_luz
    if i=="Encendido":
        GPIO.output(21,0)
        time.sleep(0.0001)
        estado_luz="Encendido"
        return(' ')
    else :
        GPIO.output(21,1)
        time.sleep(0.0001)
        estado_luz="Apagado"
        return(' ')

        

@app.route('/<string:estado_luz2>')
def home1(estado_luz2):
    
    return render_template('home.html',est=estado_luz2,A=encender)
   
   #""" t1=threading.Thread()
   # t2=threading.Thread(target=Apagado)
   # t3=threading.Thread(target=encender,args=estado_luz2)
   # if estado_luz2 == 'Encendido':
   #     t1.start()
   #     t3.start()
   #     t1.join()
   #     t3.join()
   # else :
   #     t2.start()
   #      t3.start()
   #     t2.join()
   #     t3.join()"""
    
    

        
'''#@app.route('/Encendido')
def Encedidoo(): 
   #encender('Encendido')
   return render_template ('home.html',est='Encedido',A=encender)
   

#@app.route('/Apagado')
def Apagado(): 
   encender('Apagado')
   return render_template ('home.html',est='Apagado',A=encender)'''
  


   #variuest. 
 
    
    
    
  
if __name__ == '__main__':
    
    app.run(debug=True , host= '0.0.0.0')
   # t2=threading.Thread(target=encender(estado_luz2) , args=estado_luz2)
    #t3=threading.Thread(target=apagar , args=estado_luz2)
    

    #t2.start()
    #t2.join()
    #t3.start()

    
    
    #t3.join()




