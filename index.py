#El indexraspeberry es el  uso en la rpi lo unico que agrega o modifica es el def encender 

from flask import Flask, render_template , request
import threading 
import time   
import subprocess
#Ayuda estado anterior
app = Flask(__name__)
estado_luz=""
#estado_luz2="h"
@app.route('/')
def home(): 
    
   return render_template ('home.html',est=estado_luz,A=encender) 
  
   
    
def encender(i):
    if i=="Encendido":  
        print("Encendido ctm")

        time.sleep(0.0001)
    else :
        print("Apagadp")
        time.sleep(0.0001)

def aux(s):
   global estado_luz
   estado_luz=s
   print (estado_luz)
        
#el motor.py lo unico que hace es leer el sensor para saber si esta abierto o cerrado y si se preciona algun seneor se abre o se cierrra esto no sera asi obviamente con unboton se abrira y con otro se cerrara no los sensores 
def motor():
   subprocess.call('python '+' "motor.py"  ' + 'exit()', shell=True)


@app.route('/<string:estado_luz2>')
def home1(estado_luz2):
   if (estado_luz2==("Apagado")):
      aux("Apagado")
   else:
      if (estado_luz2==("Encendido")):
        
         aux("Encendido")
         
         
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
    
    #t1=threading.Thread(target=subproceso_input)
    app.run(debug=True , host= '0.0.0.0', threaded=True)
   # t2=threading.Thread(target=encender(estado_luz2) , args=estado_luz2)
    #t3=threading.Thread(target=apagar , args=estado_luz2)
    
    #t1.start() 
    #t1.join()
    #t2.start()
    #t2.join()
    #t3.start()

    
    
    #t3.join()




