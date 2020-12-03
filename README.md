## V2.1
Version 2 Node ,ESP32,Raspberry ,IoT 
## 2.1.4
La mierdita de cambiar el estado de de la luz pero no asi el aparato
Funcionando 28 MAYO 2020
# V2.2 Configurando para el node 
se agregara una nueva libreria


## Importante 
tienes que verificar en el front end el ipfunc.json , y en el index la variable link archivos
En raspberry no funciona el dimmer
estas usando los sensores alrevess!!!!!!!!!!!11 revisa Dispositivos.py para cambiar y en la logica igual del indexrpi.py  line 1119  #######por ahoras
## Luces Cortinas Control IR
los controles IR y Lectores no sse pueden utiliazar en IoT

##Funcionando:
Falta todo disp de Nodes y Esp32 
Rasp falta lector control funcionar con todo
http://abyz.me.uk/rpi/pigpio/examples.html#Python_irrp_py


## To work in Raspberry you need to
dont use the [raspbian-nspawn-64]  Never
enable the ssh
enable I2C
sudo pigpiod

### Necesary: 
###### Mongo: (solamente la version 2.4 ya que despues no es valido para 64 bits , si instalas el raspbian nspawn no dara 05/2020 )
        sudo apt-get install mongodb -y  
        sudo apt-get install -y mongodb-server
        sudo systemctl start mongodb
        mongo
#### PARA LAS LIBRERIAS DE PY MEJOR UTILIZAR PIP3
### python-socketio   4.2.0
    pip install python-socketio
### eventlet          0.25.0
    pip install eventlet
### Flask             1.0.3
    pip install Flask
### Flask-Cors        3.0.8
    pip install Flask-Cors 
### Flask-SocketIO    4.1.0
    pip install flask-socketio
### gevent            1.4.0
    pip install gevent
### gevent-websocket  0.10.1
    pip install gevent-websocket 
### pymongo           3.9.0(windows) y version para rasp 
    pip install pymongo  or  pip install pymongo==2.4.2
### paho-mqtt         1.5.0

### ServoKit 
    sudo pip3 install adafruit-circuitpython-servokit
    
### recomend: 
###### VNC viewer: (https://www.raspberrypi.org/documentation/remote-access/vnc/) 

        sudo apt install realvnc-vnc-server realvnc-vnc-viewer
        sudo raspi-config
        Now, enable VNC Server by doing the following:

        Navigate to Interfacing Options.

        Scroll down and select VNC > Yes
###### Codeos: (https://raspberryparatorpes.net/proyectos/visual-studio-code-para-raspberry-pi/)
    sudo apt install apt-transport-https
    sudo -i
. <( wget -O - https://code.headmelted.com/installers/apt.sh )
    sudo apt install code-oss

#### Para que funcione el lector y control de IR
    sudo pigpiod



### Para que lo veas :v 
Recuerda que si lo que quieres es tener en otra máquina todo instalado 
igual que en la máquina original, lo puedes hacer con: 

$ pip freeze > requisitos.txt 

$ sudo pip install -r requisitos.txt 

el primer comando en la máquina antigua y el segundo en la nueva. 

Para saber los instalados (todos los OS) = pip list  , para saber todos los modulos (rasp) = pydoc modules
 




