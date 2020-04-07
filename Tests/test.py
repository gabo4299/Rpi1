from flask import Flask, render_template , request
from flask_socketio import SocketIO , send ,emit
import threading 
import time   
import subprocess
#Ayuda estado anterior
from gevent import monkey
monkey.patch_all()
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'
socketio = SocketIO(app ,async_mode='threading')
print ("socket abierto", socketio)

@app.route('/')
def index ():
    return render_template('test.html')

i=0



@socketio.on('mensaje')
def me(msg , e):
    print(msg + ':' + e)
    global i
#    send(msg,broadcast=True)
    emit('mensaje' ,msg , broadcast=True)
    var=msg
    t1=threading.Thread(target= funcionempezar (var) )
    t2=threading.Thread(target= funcionpara(var) )
    t1.start()
    t2.start()
    t1.join()
    t2.join()

def funcionpara(mensa):
    if mensa=='para' :
        global i
        i=1
        print('parar')

def funcionempezar(mensa):
    if mensa=='empeza':
        global i
        i=0
        while i==0:
            print(i)

            time.sleep(0.1)
        

if __name__ == '__main__':
    
    socketio.run(app,debug=True)