## V2
Version 2 Node ,ESP32,Raspberry ,IoT 

Need a lot of sudo pip3 mtf :V , pronto te lo ire poniendo perro 

## Luces Cortinas Control IR
los controles IR y Lectores no sse pueden utiliazar en IoT

##Funcionando:
Falta todo disp de Nodes y Esp32 
De rasp falta y o o funciona el Dimmer 
se anhadio el Lector Para la raspberry para q funcione !! 
http://abyz.me.uk/rpi/pigpio/examples.html#Python_irrp_py


## To work in Raspberry you need to
dont use the [raspbian-nspawn-64] 
activate the ssh
### Necesary: 
###### Mongo: (solamente la version 2.4 ya que despues )
        sudo apt-get install mongodb -y  

    
### recomend: 
** -VNC viewer: (https://www.raspberrypi.org/documentation/remote-access/vnc/) ** 

        sudo apt install realvnc-vnc-server realvnc-vnc-viewer
        sudo raspi-config
        Now, enable VNC Server by doing the following:

        Navigate to Interfacing Options.

        Scroll down and select VNC > Yes
