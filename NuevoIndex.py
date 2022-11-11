#El indexraspeberry es el  uso en la rpi lo unico que agrega o modifica es el def encender 

#pymogno installar!
'''
#instalar paho-mqtt
### todo al rapsberry arreglar hoy 3 de marzo iniciar en /main ,css background arrreglar , darle estilo a las opciones  del main , arreglar flecahas q en el celu se ve feo , ir pensando en tvs , sonos musica , camaras ,garage, osea cada cuarto tendria camaras, tvs , 
# PONER EN CLASE CUARTO NRO DE PINES AGREGAR CLASE CUARTO 
#agregar clases controles , garajes,tipos de garajes , mas nodes ,
#intentar con foot resistencia o en todo caso con una rpi zero 
## hacerlo todo al mismo tiempo leer sensores ! 
#mira gil necesitas hacer lo de radio frecuencia para abrir garajes 
#para leer estados de luz primero necesitamos que se peuda activar 
# .... la luz desde el interruptor esto con un or sensillo que se hace con didos fijate este link 
#https://www.youtube.com/watch?v=HZP6pSXM-aM
#y con eso tenemos 2 pulsadores sin necesidad de otra placa 
# aahora para leerlo es la joda  :v  puedes leer el resultado  con puta nose 
'''
import json
import multiprocessing
from flask import Flask, render_template , request, jsonify
from flask_socketio import SocketIO , send  , emit
import threading 
import time   
import subprocess
import array
from eventlet import tpool
from flask_mqtt import Mqtt

import eventlet
eventlet.monkey_patch()
from Base import Cortina,Cuarto,Interruptor
#from Dispositivos import Raspberry
#### si utilizas la rasp es Operacionees sino es el otro OperacionesWind
#from Operaciones import OpCortina,OpCuarto,OpInterruptor,OpCasa,OpControl,OpMarcaControl,OpLecIR,OpNode,OpRasp,OpEsp32
from OperacionesWind import OpCortina,OpCuarto,OpInterruptor,OpCasa,OpControl,OpMarcaControl,OpLecIR,OpNode,OpRasp,OpEsp32
from flask_cors import CORS, cross_origin
#instalar uploader filename
import os
from flask import send_file
from werkzeug.utils import secure_filename
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
app = Flask(__name__)
# para mqtt 
app.config['MQTT_BROKER_URL'] = '127.0.0.1'
app.config['MQTT_BROKER_PORT'] = 1883   
app.config['MQTT_REFRESH_TIME'] = 1.0  # refresh time in seconds

mqtt = Mqtt(app)
mqtt.subscribe('node/giveme')

cont=1

global DirFondos
# UPLOAD_FOLDER ='Images/Fondos'
# UPLOAD_FOLDER= "C:\Users\gabri\Documents\Domotica Empezamos !\Prueba para tio raspberrry\Images\Fondos"
#################################################### WINDOWS###############
LinkArchivos=r"C:\Users\gabri\Documents\Domotica Empezamos !\Prueba para tio raspberrry\Images\Fondos\Fondo"
LinkArchivosDefault=r"C:\Users\gabri\Documents\Domotica Empezamos !\Prueba para tio raspberrry\Images\Fondos\Default.png"
##################################################   RASP   #############
#LinkArchivosDefault=r"/home/pi/Desktop/Rpi1/Images/Fondos/Default.png"
#LinkArchivos=r"/home/pi/Desktop/Rpi1/Images/Fondos/Fondo"
LecturaDeSensores={}
UPLOAD_FOLDER= "./Images/Fondos/"
app.config['SECRET_KEY']='secret'
app.config['UPLOAD_FOLDER']=UPLOAD_FOLDER

#tener un array de todas las luces y ese va ser dato entonces e dice en q posiciones va a haber un true o false 
def LuzEncenderApagar(posicion,cambio,array):
    #entonces aqui la posicion es al numero que queires llegar 
    print ("Enciendes este")
        


# CORS(app, sources=r'/API/*')
CORS(app, resources={r"/api/*": {"Access-Control-Allow-Origin": "*"}})
socketio=SocketIO(app,async_mode='eventlet')
socketio.init_app(app, cors_allowed_origins="*")

#falta en (app,async mode='threading") 
#nota sin el async mode no se puede parar el programa con cntrol c , pero si es en tiempo real !
# suscribimos a el canal del node 


@mqtt.on_message()
def handle_mqtt_message(client, userdata, message):
    data = dict(
        topic=message.topic,
        payload=message.payload.decode()
    )

    # print( data["topic"])
    if data["topic"] == "node/giveme":
        
        # print (data["payload"])
        MESAGEMQTT= (data["payload"])
        MESAGEMQTT = str(MESAGEMQTT)
        MESAGEMQTT = json.loads(MESAGEMQTT)
        # print ( mes2car["id"])
        if MESAGEMQTT["id"] >0: # osea si esque es el id 
            idNode = int(MESAGEMQTT["id"])
            if OpNode().buscarNode(idNode): #buscar id 
                print ("existe")
                link1= "node/"+str(idNode)+"/setIN" 
                link1= "node/"+str(idNode)+"/setIN" 
                link1= "node/"+str(idNode)+"/setIN" 
                link1= "node/"+str(idNode)+"/setIN" 
#si existe entonces mandarle los pines de salida de entrada y de tv 
                # empeazar a madar los pines  OUT IN OUX 
            else:
                print ("no existe")
            
            print (MESAGEMQTT["id"])

        



        
    # funcioana
    # if data[topic] == "node/giveme":
    #     print ("me estas giveando")


@app.route('/')
@cross_origin()
def home():
    return render_template('home2.html')
encendiendo='1'

def imprimirsi():
    a=OpInterruptor().buscarIdInterruptor(1)
    
    #print (a['Estado'] , "holaaaaaaaaaaaaaaaaaaaaaaadebug")
    
    if a['Estado'] == 'Encendido':
        while a['Estado'] == 'Encendido':
            a=OpInterruptor().buscarIdInterruptor(1)
            print("sii estado:" ,   a['Estado'] )
            time.sleep(0.1)
    else:
        print ("ok")

##############################  Casa#########################
@app.route('/API/Casa')
def Casas():
    js = jsonify(OpCasa().MostrarCasas())
    return js 

@app.route('/API/Casa/ID')
def casasID():
    print (OpCasa().MostrarIds())
    js = jsonify(OpCuarto().MostrarIds())
    return js 

@app.route('/API/Casa/<string:idcasa>')
def apiCasa(idcasa):
    if (OpCasa().buscaridcasa(idcasa)== True):
        idcasa=int(idcasa)
        aux=OpCasa().MostrarCasaEsp(idcasa)        
        return jsonify(aux)
    else:
        return ("No Existe Casa")

@app.route('/API/Casa/add' , methods=['POST'])
def addCasa():
    a=OpCasa().insertarCasa(request.json["IdCasa"],request.json["Nombre"],"")
    return (a)

@app.route('/API/Casa/<string:idcasa>/del' , methods=['DELETE'])
def delCasa(idcasa):
    if OpCasa().buscaridcasa(idcasa)==True:
        idcasa=int(idcasa)

        
        return OpCasa().eliminarCasa(idcasa)
    else :
        return('no existe id ')

@app.route('/API/Casa/<string:idcuarto>/mod' , methods=['PUT'])
def modCasa(idcuarto):
    
    if OpCasa().buscaridcasa(idcuarto)==True:
        idcuarto=int(idcuarto)
        
   
        if request.form["Nombre"]!='' and request.form["Nombre"]!=' ':
            return (OpCasa().modificarCasa(idcuarto,"Nombre",request.form["Nombre"]))
        if request.form["Ports"]!='' and request.form["Ports"]!=' ':
            return (OpCasa().modificarCasa(idcuarto,"Ports",request.form["Ports"]))
        if request.form["Ip"]!='' and request.form["Ip"]!=' ':
            return (OpCasa().modificarCasa(idcuarto,"Ip",request.form["Ip"]))



##################### Cuartos###################


@app.route('/API/Cuartos')
def cuartos():
    # print (OpCuarto().MostrarCuartos())
    js = jsonify(OpCuarto().MostrarCuartos())
    
    return js 

@app.route('/API/Cuartos/ID')
def cuartosID():
    print (OpCuarto().MostrarIds())
    js = jsonify(OpCuarto().MostrarIds())
    return js 

@app.route('/API/Cuarto/<string:idcuarto>')
def apiCuarto(idcuarto):
    if (OpCuarto().buscaridcuarto(idcuarto)== True):
        idcuarto=int(idcuarto)
        aux=OpCuarto().MostrarCuartoEsp(idcuarto)
        
        print (aux)
        
        return jsonify(aux)
    else:
        print("no existe ")
        return ('no existe Cuarto')

@app.route('/API/Cuarto/add' , methods=['POST'])

#@cross_origin()
#@cross_domain(origin='*')
def add():
    
    a=OpCuarto().LastID()
    a=a+1
    if  a >=0 :       
            #print(request.form['Seleccion'] ,"este es el select ")
            if(request.form['Seleccion']=='Si'):
                file=request.files['fondo']
                if file and allowed_file(file.filename):
                        print("entro")
                        f = request.files['fondo']
                        concadenacion="Fondo"+request.form['nombre']+'.jpg'
                        filename=secure_filename(concadenacion)
                        f.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
                        ruta=LinkArchivos
                        ruta=ruta+request.form["nombre"]+".jpg"
                return jsonify(OpCuarto().insertarCuarto(a,request.form["idcasa"],request.form['nombre'],ruta,request.form['contrasenha']))
            else:
                return jsonify(OpCuarto().insertarCuarto(a,request.form["idcasa"],request.form['nombre'],'No',request.form['contrasenha']))


@app.route('/API/Cuarto/<string:idcuarto>/del' , methods=['DELETE'])
def dele(idcuarto):
    print ("El resutado del delete es",OpCuarto().buscaridcuarto(idcuarto))
    if OpCuarto().buscaridcuarto(idcuarto)==True:
        idcuarto=int(idcuarto)
        
        print ("Debuggg Delete", OpCuarto().eliminarCuarto(idcuarto))
        return ("eliminado satisfactoriamente")
    else :
        return('no existe id ')

@app.route('/API/Cuarto/<string:idcuarto>/mod' , methods=['PUT'])
def mod(idcuarto):
    
    if OpCuarto().buscaridcuarto(idcuarto)==True:
        idcuarto=int(idcuarto)
        
   
        if request.form["nombre"]!='' and request.form["nombre"]!=' ':
            OpCuarto().modificarCuarto(idcuarto,"nombre",request.form["nombre"])
  
        if request.form["contrasenha"]!='' and request.form["contrasenha"]!=' ' or request.form['QuitarContra']=='Si':
            OpCuarto().modificarCuarto(idcuarto,"contrasenha",request.form["contrasenha"])
        # if request.form["NDispositivos"]!='' and request.form["NDispositivos"]!=' ':
        #     OpCuarto().modificarCuarto(idcuarto,"NDispositivos",request.form["NDispositivos"])


        if(request.form['Seleccion'])=='Si':
            print("entro a fondo")
            file=request.files['fondo']
            if file and allowed_file(file.filename):
                            print("entro")
                            f = request.files['fondo']
                            concadenacion="Fondo"+OpCuarto().MostrarCuartoEsp(idcuarto)['nombre']+'.jpg'
                            filename=secure_filename(concadenacion)
                            f.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
                            ruta=LinkArchivos
                            ruta=ruta+OpCuarto().MostrarCuartoEsp(idcuarto)['nombre']+".jpg"
                            OpCuarto().modificarCuarto(idcuarto,'fondo',ruta)
            else:
                    OpCuarto().modificarCuarto(idcuarto,"fondo",'No')
                    return("Error Imagen Se restablecio")

            

                

            
        return "completado"

    else:
        return 'No existe el Cuarto con el id '


@app.route('/API/Cuarto/<string:idcuarto>/Fondo')
def fondo(idcuarto):
    if OpCuarto().buscaridcuarto(int(idcuarto)):
        x=OpCuarto().MostrarCuartoEsp(int (idcuarto))
        print (x["idcuarto"])
        if (x["fondo"]=="No" or x["fondo"]=="n" or x["fondo"]=="None" or x["fondo"]=="none" ):
            filename=LinkArchivosDefault
            return send_file(filename,mimetype='image/gif')
        else:
            filename=x["fondo"]
            return send_file(filename, mimetype='image/gif')
    else:
        return ("No existe Cuarto")
@app.route('/API/Cuarto/Fondo')
def fondodef():
    filename=LinkArchivosDefault
    return send_file(filename,mimetype='image/gif')


############################# Subir Imagenes Prueba ########################################

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/API/Uploader', methods = [ 'POST'])
def upload_file():

   if request.method == 'POST':
    #  print( "esta es la request " , request.form['Nombre'])
     file = request.files['fondo']
     if file and allowed_file(file.filename):
        f = request.files['fondo']
        filename=secure_filename('FondoNombre.jpg')
        f.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
        return 'file uploaded successfully'



############################Garages##################################
###########################Controles##############################
############################Musica###############################
###########################Alexa################################


#########################   Luces    ################


@app.route('/API/Luces')
def luces():
    print (OpInterruptor().MostrarInterruptores())
    js = jsonify( OpInterruptor().MostrarInterruptores())
    return js 

@app.route('/API/Cuarto/<string:idcuarto>/Luz/<string:idLuz>')
def Apiluz(idLuz,idcuarto):

    #print(idcuarto )
    #print (idLuz)
    aux=OpInterruptor().buscarIdInterruptor(idLuz)
    jsonify (aux)
    if aux!=0:
        if  aux['IdCuarto']==int(idcuarto):
            return jsonify (OpInterruptor().buscarIdInterruptor(idLuz))
        else:
            return('error de cuarto')
    else:
        if aux==0:
            return ('NO EXISTE INTERRUPTOR')

@app.route('/API/Cuarto/<string:idcuarto>/Luz/<string:idluz>/Estado' ,methods=['POST','GET'])

def estadoLuz(idcuarto,idluz):
    idluz=int(idluz)
    aux=OpInterruptor().buscarIdInterruptor(idluz)
    jsonify (aux)
    
    if aux!=0:
        if request.method == "POST":
            if aux["Dimmer"] == False:
                if request.json['Estado']== 1 or request.json['Estado']=='Encendido':
                    OpInterruptor().modidificarEstadoiNT(idluz,'Encendido')
                    ####funcion cambio de luz de idluz a encender
                    socketio.emit('LuzCambio', (int(idluz),"Encendido"))
                    
                                   
                    # tpool.execute(imprimirsi)
                    # imprimirsi()
                    # print ("Encendido luz ",idluz,"gracias")
                    msg ="Encendido luz"  +str (idluz)+"gracias"
                    return (msg)
                else:
                    if request.json['Estado']== 0 or request.json['Estado']=='Apagado':
                        OpInterruptor().modidificarEstadoiNT(idluz,'Apagado')
                        # imprimirsi()
                        socketio.emit('LuzCambio', (int(idluz),"Apagado"))
                        msg ="Apagando luz"  + str(idluz)+"gracias"
                        return (msg)
                    else:
                        return("negativo")
            else:
                        OpInterruptor().modidificarEstadoiNT(idluz,request.json['Estado'])
                        # con t pool tendras que encender :V 
                        socketio.emit('LuzCambio', (int(idluz),request.json['Estado']))
                        msg ="Dimmeando luz id: "  + str(idluz)+" al :",str(request.json["Estado"]) +"'%' gracias"
                        print (msg) 
                        return ("Complete")
        else:
            if request.method== "GET":
                a=OpInterruptor().buscarIdInterruptor(idluz)
                js=jsonify(a["Estado"])
                return js
        

            
        
    else:
        if aux==0:
            return ('NO EXISTE INTERRUPTOR')


@app.route('/API/Cuarto/<string:idcuarto>/Luz/<string:idluz>/Onlystate/<string:estado>')
def CambiarSoloEstado(idcuarto,idluz,estado):
    idluz=int(idluz)
    print ("entro")
    aux=OpInterruptor().buscarIdInterruptor(idluz)    
    if aux!=0:
        
        if aux["Dimmer"] == False:
            if estado == "Apagado" or estado == 0 :
                OpInterruptor().modidificarEstadoiNT(idluz,'Apagado')
                socketio.emit('LuzCambio', (int(idluz),"Apagado"))
                msg ="Estado luz Apagado"  + str(idluz)+"gracias"
                return (msg)
            if estado == "Encendido" or estado == 1 :
                OpInterruptor().modidificarEstadoiNT(idluz,'Encendido')
                socketio.emit('LuzCambio', (int(idluz),"Encendido"))
                msg ="Estado  luz Encendido"  + str(idluz)+"gracias"
                return (msg)
        else:
            return ("Es dimmer error")
    else:
        return ("no existe")
@app.route('/API/Cuarto/<string:idcuarto>/Luz/<string:idluz>/Invertrele')
def InvertirElRele(idcuarto,idluz):
    idluz=int(idluz)
    aux=OpInterruptor().buscarIdInterruptor(idluz)    
    if aux!=0:
        
        if aux["Dimmer"] == False:
            if aux["SalidaRele"] == 0:
                OpInterruptor().modidificarEstadoRele(idluz,1)
                return ("OK")
                ####LA HUEVADA PARA CAMBIAR 
            if aux["SalidaRele"] ==1:
                OpInterruptor().modidificarEstadoRele(idluz,0)
                return ("OK")
                ####LA HUEVADA PARA CAMBIAR  
 
@app.route('/API/Cuarto/<string:idcuarto>/Luz/add', methods=['POST'])
def addI(idcuarto):
    idcuarto=int(idcuarto)
    
    
    # print (request.json)
    ids = OpInterruptor().LastID() +1
    if (OpCuarto().buscaridcuarto(idcuarto)== True) :

         a=OpInterruptor().insertarInterruptor(ids  ,request.json["IdDisp"],request.json["Dispositivo"],idcuarto,request.json["Pin"],request.json["Dimmer"],request.json["Nombre"])

         return (a)
    else:
         return('error de cuarto')

@app.route('/API/Cuarto/<string:idcuarto>/Luz/<string:idLuz>/mod', methods=['PUT'])
def modI(idcuarto,idLuz):
    idcuarto=int(idcuarto)
    idLuz=int(idLuz)
    if (OpCuarto().buscaridcuarto(idcuarto)== True):
        aux=OpInterruptor().buscarIdInterruptor(idLuz)
        jsonify(aux)
        cont=0
        mesg=""
        if aux!=0:

            if request.json["Pin"] != '' and request.json["Pin"] != ' ':
                cont = cont +1
                mesg=mesg+" Se cambio el Pin : " + OpInterruptor().modInterruptor(idLuz,"Pin",request.json["Pin"])
                
            if request.json["Nombre"] != '' and request.json["Nombre"] != ' ':
                cont = cont +1
                mesg=mesg+" Se cambio el Nombre : " +   OpInterruptor().modInterruptor(idLuz,"Nombre",request.json["Nombre"])
            if cont == 0 : 
                return ( "No se realizaron Modificaciones")
            else :
                last_mes= "Se realizaron "+str(cont)+" Modificaciones , " + mesg
                return (last_mes)
            

            
        else:
            return "no existe interruptor con este id"
    else:
        return ('no existe Cuarto')

@app.route('/API/Cuarto/<string:idcuarto>/Luz/<string:idLuz>/del', methods=['DELETE'])
def delInt(idcuarto,idLuz):
    if OpCuarto().buscaridcuarto(idcuarto)==True:
        idcuarto=int(idcuarto)
        idLuz=int(idLuz)
        if OpInterruptor().buscarIdInterruptor(idLuz) != 0:
            OpInterruptor().EliminarInterruptor(idLuz)
            return "eliminado satisfactoriamente"
        else:
            return "No existe interruptor con ese id"
    else :
        return('no existe cuarto con ese id ')



#################### Cortinas#################


@app.route('/API/Cortinas')
def cortinas():
    print (OpCortina().MostrarCortinas())
    js = jsonify( OpCortina().MostrarCortinas())
    return js 



@app.route('/API/Cuarto/<string:idcuarto>/Cortina/<string:IdCortina>')
def ApiCortina(IdCortina,idcuarto):
    
    aux=OpCortina().buscarIdCortina(IdCortina)
    jsonify (aux)
    if aux!=0:
        if  aux['IdCuarto']==int(idcuarto):
             return jsonify (OpCortina().buscarIdCortina(IdCortina))
        else:
                return('error de cuarto') 
    else:
            if aux==0:
                return ('NO EXISTE cortina')


@app.route('/API/Cuarto/<string:idcuarto>/Cortina/add', methods=['POST'])
def addcor(idcuarto):
    if OpCuarto().buscaridcuarto(idcuarto)==True:
        idcuarto=int(idcuarto)
        idcort=OpCortina().LastID() +1
        # print (request.json)
        b=OpCortina().insertarCortina(idcort,idcuarto,request.json["IdDisp"],request.json["Dispositivo"],request.json["Pinmotor"],request.json["PinSensor1"],request.json["PinSensor2"],request.json["Tipo"],request.json["Nombre"])
        return (b)
    else :
        return('no existe id de caurto ')


@app.route('/API/Cuarto/<string:idcuarto>/Cortina/<string:IdCortina>/del',methods=['DELETE'])
def delCor(idcuarto,IdCortina) :
    idcuarto=int(idcuarto)
    if OpCuarto().buscaridcuarto(idcuarto)==True:
        IdCortina=int(IdCortina)
        if (OpCortina().buscarIdCortina(IdCortina)!=0):
            
            OpCortina().EliminarCortina(IdCortina)
            return ("eliminado satisfactoriamente")
        else:
            return ("error no se ecuentra id ")
    else :
            return('no existe id de caurto ')    

@app.route('/API/Cuarto/<string:idcuarto>/Cortina/<string:IdCortina>/mod' , methods=['PUT'])
def modcor(idcuarto,IdCortina):
        if OpCuarto().buscaridcuarto(idcuarto)==True:
            idcuarto=int(idcuarto)
            mesaggeReturn=""
            cont = 0
            if request.json["Nombre"]!='' and request.json["Nombre"]!=' ':
                cont=cont +1
                mesaggeReturn=mesaggeReturn+ " Se cambio el nombre: " + OpCortina().modcortina(int(IdCortina),"Nombre",request.json["Nombre"])
                

            if request.json["Pinmotor"]!='' and request.json["Pinmotor"]!=' ':
                cont=cont +1
                mesaggeReturn=mesaggeReturn+ ", Se cambio el Pin del Motor: " + OpCortina().modcortina(IdCortina,"Pinmotor",request.json["Pinmotor"])
                
            if request.json["PinSensor1"]!='' and request.json["PinSensor1"]!=' ':
                cont=cont +1
                mesaggeReturn=mesaggeReturn+ ", Se cambio el Pin del Sensor 1: " + OpCortina().modcortina(IdCortina,"PinSensor1",request.json["PinSensor1"])
                
            if request.json["PinSensor2"]!='' and request.json["PinSensor2"]!=' ':
                cont=cont +1
                mesaggeReturn=mesaggeReturn+ ", Se cambio el Pin del Sensor 2: " + OpCortina().modcortina(IdCortina,"PinSensor2",request.json["PinSensor2"])                                
                
            if request.json["Tipo"]!='' and request.json["Tipo"]!=' ':
                cont=cont +1
                mesaggeReturn=mesaggeReturn+ ", Se cambio el Pin del Sensor 2: " + OpCortina().modcortina(IdCortina,"Tipo",request.json["Tipo"]) 
                
            if cont == 0 :
                return ("No se realizaron Modificaciones")

            else:
                el_utlimo="Se realizaron " + str(cont) +" Modificaciones "+mesaggeReturn
                return (el_utlimo)

            

        else:
           return 'No existe el caurto con el id '

@app.route('/API/Cuarto/<string:idcuarto>/Cortina/<string:IdCortina>/Estado' ,methods=['GET', 'POST'])
def estadocor(idcuarto,IdCortina):
    if OpCuarto().buscaridcuarto(idcuarto)==True:
        
            idcuarto=int(idcuarto)
            IdCortina=int(IdCortina)
            if OpCortina().buscarIdCortina(IdCortina)!=0:
                if request.method == 'POST':
                    if request.json["Cambiar"]=="Si" :
                        if request.json["Estado"]== 'Abierto':
                            print("subir completamente  id:" , int(IdCortina))
                            OpCortina().modidificarEstadoCortina(IdCortina,'Abierto')
                            socketio.emit('CortinaCambio', (int(IdCortina),request.json["Estado"]))
                            
                            return ("Estado Cambiador a Abierto")
                        if request.json["Estado"]== 'Semi':
                            print("Subir bajar  UN poco  parametros")
                            OpCortina().modidificarEstadoCortina(IdCortina,'Semi')
                            socketio.emit('CortinaCambio', (int(IdCortina),request.json["Estado"]))
                            return ("Estado Cambiador a Semi")
                        if request.json["Estado"]== 'Cerrado':
                            print("Bajar completamente ")
                            OpCortina().modidificarEstadoCortina(IdCortina,'Cerrado')
                            socketio.emit('CortinaCambio', (int(IdCortina),request.json["Estado"]))
                            return ("Estado Cambiador a Cerrado")   
                    else:
                        if request.json["Estado"]== 'Abierto':
                            print("subiendo hacer sub la cortina ")
                            return("subiendo hacer sub la cortina ")
                        if request.json["Estado"]== 'Cerrado':
                            print("bajado hacer bajar la cortina ")
                            return("bajado hacer bajar la cortina ")
                        if request.json["Estado"]== 'Semi':
                            print("Subir bajar  UN poco  parametros")
                            return("Subir bajar  UN poco  parametros")

                else:
                    if request.method == 'GET':
                        
                        a = OpCortina().buscarIdCortina(IdCortina)
                        js= jsonify(a['Estado'] )
                        #print ()
                        #print (js)
                        return (js)
            else:
                return ("no existe cortina con id ")
    else:
        return ("NO EXISTE ID DE CUARTO")


##########3###############################Controlador Mcu#########################
@app.route('/API/CPU/<string:Disp>/<string:id>')
def delvolverDispositvo(Disp,id):
    if Disp == "Node":

        js = jsonify(OpNode().MostrarNodeEsp(int(id)))
        return js 
    if Disp == "Rasp":
        js = jsonify(OpRasp().MostrarRaspEsp(int(id)))
        return js 
    if Disp == "Esp32":
        js = jsonify(OpEsp32().MostrarESP32Esp(int(id)))
        return js 
    if Disp == "IoTs":
        js = jsonify(OpEsp32().MostrarESP32Esp(int(id)))
        return js 
    else :
        return ("Error de Dispositvo")

@app.route('/API/CPU/Node/<string:id>/conf')
def ConfNode(id):
    if OpNode().buscarNode(int(id)):
        # enviar con paho y escuchar si es necesario
        print  ("OK")
    else:
        return ("No se registro Node")
@app.route('/API/CPU/Esp32/<string:id>/conf')
def ConfEsp32(id):
    if OpEsp32().buscarEsp32(int(id)):
        # enviar con paho y escuchar si es necesario
        print  ("OK")
    else:
        return ("No se registro Node")
@app.route('/API/CPU/<string:Disp>' )
def Dispst(Disp):
    if Disp == "Rasps":
        
        js = jsonify( OpRasp().MostrarRasps())
        return (js)
    else :
        if Disp == "Nodes":
            if OpNode().MostrarNodes() != {}:
                js=jsonify(OpNode().MostrarNodes())
                print ("Debugueannnnnnnnnnnnndo",js)
                return (js)
            else :
                return "No se registraron"
        if Disp == "Esp32s":
            if OpEsp32().MostrarEsp32s != {}:
                js=jsonify(OpEsp32().MostrarEsp32s())
                print ("Debugueannnnnnnnnnnnndo",js)
                return (js)
            else :
                return "No se registraron"
            

@app.route('/API/CPU/<string:Disp>/add' , methods=['POST'])
def addDisp(Disp):
    val=request.json
    if Disp == "Rasp":
        
        
        j= (OpRasp().InsertarRasp(int(val["IdRasp"]),val["IdCasa"],int(val["CantidadPWM"]),int(val["CantidadLuz"]), val["IoT"],val["Descripcion"]))
        return j
    if Disp == "Node":
        js = (OpNode().InsertarNode(int(val["IdNode"]),int (val["IdCasa"]),val["Descripcion"]))
        return (js)
    if Disp == "Esp32":
        js = (OpEsp32().InsertarEsp32(int(val["IdEsp32"]),int (val["IdCasa"]),val["Descripcion"]))
        return (js)
    else:
        return ("Error")
    


        

@app.route('/API/CPU/<string:Disp>/<string:id>/del' , methods=['DELETE'])
def delDisp(Disp,id):
    id = int (id)
    if Disp == "Rasp":
        if OpRasp().buscarRasp(id):
            return (OpRasp().ElmiminarRasp(id))
        else :
            return('no existe id ')
    if Disp == "Node":
        if OpNode().buscarNode(id):
            return (OpNode().ElmiminarNode(id))
        else :
            return('no existe id ')
    if Disp == "Esp32":
        if OpEsp32().buscarEsp32(id):
            return (OpEsp32().EliminarEsp32(id))
        else :
            return('no existe id ')
    return("Error Dispositivo")

@app.route('/API/CPU/<string:Disp>/<string:id>/PinFree/<string:tipo>')
def PinsLibres(Disp,id,tipo):
    id = int (id)
    if Disp == "Rasp":
        if OpRasp().buscarRasp(id):
            return ( jsonify(OpRasp().DevolverPinsLibres(id)) )
        else :
            return('no existe id')
    if Disp == "Node":

        if OpNode().buscarNode(id):
            if tipo =="analog":
                return (jsonify(OpNode().devolverAnalogicoLibre(id)))
            else:

                return jsonify(OpNode().DevolverPinsLibres(id))
        else :
            return('no existe id')
    if Disp == "IoT":
        if OpRasp().ComprobarIoT(id):
            if tipo == "PWM":
                return (jsonify(OpRasp().DevolverPinIoT(id,"PWM")))
            if tipo == "Luz":
                return (jsonify(OpRasp().DevolverPinIoT(id,"L")))
            if tipo =="Sen":
                return (jsonify(OpRasp().DevolverPinIoT(id,"S")))
            
        else :
            return('no existe id')
    if Disp == "Esp32":
        if OpEsp32().buscarEsp32(id):
            return (jsonify(OpEsp32().DevolverPinsLibres(id)))
        else :
            return('no existe id')


#######################################LecIR###################################33
@app.route('/API/LecIR/add' , methods=["POST"])
def addLecIR():
    val=request.json
    #idlec autoincrementable#iddisp elegis #idcasa 1 #disp elegis # pin lista
    if val["Dispositivo"] != "Rasp" and val["Dispositivo"] != "Node" and val["Dispositivo"] != "Esp32":
        return ("Error Dispositivo No valido")
        
    else:
        id=OpLecIR().LastID()
        if id == "No Existen":
            id=0
            if val["Dispositivo"]=="Node":
                
                return (OpLecIR().InsertarLector(id,int(val["IdDisp"]),int(val["IdCasa"]),val["Dispositivo"],val["Pin"]))
            else:
                return (OpLecIR().InsertarLector(id,int(val["IdDisp"]),int(val["IdCasa"]),val["Dispositivo"],int(val["Pin"])))
        else :
            id=id+1
            if val["Dispositivo"]=="Node":
                
                return (OpLecIR().InsertarLector(id,int(val["IdDisp"]),int(val["IdCasa"]),val["Dispositivo"],val["Pin"]))
            else:
                return (OpLecIR().InsertarLector(id,int(val["IdDisp"]),int(val["IdCasa"]),val["Dispositivo"],int(val["Pin"])))
        
    
    

@app.route('/API/LecIR/<string:id>')
def getLecIR(id):
    lec=OpLecIR().BuscarLector(int(id))
    if lec == 0 :
        return ("No existe Lector con este ID")
    else :
        return jsonify(lec)

@app.route('/API/LecIR/<string:id>/del' , methods=["DELETE"])
def delLecIR(id):
    return jsonify(OpLecIR().EliminarLector(int (id)))

@app.route('/API/LecIRS' )
def LecIRS():
    return (jsonify(OpLecIR().MostrarControles()))


@app.route('/API/LecIR/<string:id>/data')
def leerIR(id):
    print ("necesitas hacer para leer este en x dispositivo  y q te retorne el dato ! ")

#######################################Control y Marca##########################
@app.route('/API/ControlIR/add' , methods=["POST"])
def addConrolIR():      
    val=request.json
    IdControl=OpControl().LastID()+1
    
    if (val["Guardar"] == False or val["Guardar"] == "False"):
        
        return (OpControl().InsertarControl(IdControl,val["IdDisp"],val["Marca"],val["Dispositivo"],val["Pin"],val["Nombre"],val["IdCuarto"],False,val["Tipo"]))
    else:
        return (OpControl().InsertarControl(IdControl,val["IdDisp"],val["Marca"],val["Dispositivo"],val["Pin"],val["Nombre"],val["IdCuarto"],True,val["Tipo"]))

@app.route('/API/ControlIR/<string:id>')
def getConrolIR(id):
    lec=OpControl().BuscarControl(int(id))
    if lec == 0 :
        return ("No existe Lector con este ID")
    else :
        return jsonify(lec)


@app.route('/API/ControlIR/<string:id>/copyMarca' ,methods=["POST"])
def AsociarMarca(id):
    lec=OpControl().BuscarControl(int(id))
    data=request.json
    if lec == 0 :
        return ("No existe Lector con este ID")
    else :
        return OpControl().CopiarMarca(int(id),data["Marca"])
        

@app.route('/API/Controles')
def getAllLecIR():
    
    return jsonify(OpControl().MostrarControles())
@app.route('/API/Marca')
def getMarcas():
    return jsonify(OpMarcaControl().MostrarMarcas())



@app.route('/API/Marca/<string:name>')
def getMarca(name):
    return (OpMarcaControl().BuscarMarcaNombre(name))

@app.route('/API/ControlIR/<string:id>/<string:Marc>/del' , methods=["DELETE"])
def delConrolIR(id,Marc):
    if int(Marc)==1:
        return (OpControl().ElimnarControl(int (id),True))
    else:
        if int(Marc)==0:
            return (OpControl().ElimnarControl(int (id),False))
    
@app.route('/API/ControlIR/<string:id>/mod',methods=["PUT"])
def ModControl(id):
    control =OpControl().BuscarControl(int(id))
    data=request.json
    cont = 0 
    mes1 = ""
    if control!=0:
        if data["Nombre"] != "" and data["Nombre"] != " "  :
            s=OpControl().ModificarControl(int(id),"Nombre",data["Nombre"])
            cont = cont +1
            mes1=mes1+" Nombre :"+s
        if data["Tipo"] != "" and data["Tipo"] != " " :
            a=OpControl().ModificarControl(int(id),"Tipo",data["Tipo"])
            cont = cont +1
            mes1=mes1+" Tipo :"+a
        if data["Pin"] != "" and  data["Pin"] != " "  :
            p=OpControl().ModificarControl(int(id),"Pin",int(data["Pin"]))
            cont = cont +1
            mes1=mes1+" Pin :"+p
        
        if data["Marca"] != control["Marca"]:
                
                if data["Marca"]=="":
                    e=OpControl().EliminarMarcaControl(int (id))
                    mes1=mes1+" Marca :"+ e
                else:
                    if data["Create"] == 1:
                        e=OpControl().RegistrarMarca(int (id),data["Marca"])
                    else :
                        e=OpControl().CopiarMarca(int (id),data["Marca"])
                    mes1=mes1+" Marca :"+ e
                cont = cont +1
                
        # mes= "Se registraron "+ (str(cont)) + "Cambios, " +mes1
        dit={
            "CantidadCambios":cont,
            "Message":mes1
        }
        print (dit)
        return jsonify(dit)

    else:
        return("Error no existe Control")




@app.route('/API/ControlIR/<string:id>/delCode/<string:NameCommand>' )
def DeleteCodigoControl(id,NameCommand):
    e=OpControl().BorrarCodigo(int(id),str(NameCommand))
    return jsonify(e)

@app.route('/API/ControlIR/<string:id>/delAllCodes',methods=["PUT"] )
def DeleteAllCodesControls(id):
    data=request.json
    if data["Marca"] == "true" or data["Marca"]==True:
        e=OpControl().BorrarTodosCodigos(int(id),True)
        return jsonify(e)
    else:
        e=OpControl().BorrarTodosCodigos(int(id),True)
        return jsonify(e)



@app.route('/API/ControlIR/<string:id>/send/<string:NameCommand>')
def mandarIR(id,NameCommand):
    cont =OpControl().BuscarControl(int(id))
    if cont!=0:
        
        if cont["Codigos"][NameCommand]:
            print("Si existe necesitas ahora envairlo al rasp" )
            return ("Si existe") 
        else :
            return ("No se registro Codigo")
    else:
        return("Error no existe Control")
@app.route('/API/ControlIR/<string:id>/LecIR/<string:LecIR>/<string:Name>')
def RegistrarCodigo(id,LecIR,Name):
    #empiezas a leer codigo y un while true 
    # byte =leerIR(int(LecIR))
    #empiezs un subproceso
    # el socketemit'LecturaControlIR'
    socketio.start_background_task(LecturaControlIR)
    return OpControl().AddCodigo(int(id),Name,"byte")


def LecturaControlIR():
    guardar=False
    
    while (guardar == False):
        with open('Lector/EstadoControl.json', 'r') as file:
            Cods = json.load(file)
        socketio.emit('LecturaControlIR',Cods)
        
        if Cods["Guardado"]==True:
            guardar=True
        eventlet.sleep(0.02)
                
######webas?#######3
@app.route('/API/Node/<string:ID>')
def compNode(ID):

    if OpNode().buscarNode(ID)==True:
        n=OpNode().MostrarNodeEsp(int (ID))
        if n["Estado"] !="Activado":
            OpNode().CambiarEstado(ID)
        Libres=(OpNode().DevolverPinsOcupados(ID))
        print (Libres)
        for k,v in  (Libres.items()) :
            print ("Enviando : ",k ," Pin: ",v)
            data={
                "Pin":int (k),
                "Mode":v
            }
            data=json.dumps(data)
            
            link="node/"+str(ID)+"/SET"
            mqtt.publish(link, data)

        #Tambien lo activas
        # print (len(OpNode().DevolverPinsLibres(ID)))
        return ("Si")
        # aQUI PUBLICAS N veces los pines 
        # armar estructura facha 
    return ("No")

@app.route('/API/Node/<string:ID>/mqtt')
def RegNode():
    # vamos registrando 
    #     mes = {"message":"yes"}
    # return(jsonify(mes))
    # return(jsonify("{message:'yes'}"))
    return ("Si")

KillearHilo={}
####par aq func el multiproces
# import serial
# arduino = serial.Serial('COM3', 9600)
# @app.route('/API/Potencia/<string:poten>')
# def potecia(poten):
#     if not arduino.isOpen():
#         arduino.open()
#     val=int (poten)
#     val=100-val
#     arduino.write(val+10)
    
    
#     return ("ok")


@socketio.on("Estado_Cortinas_Cuarto")
def LeerSensoresCuarto(idcuarto,IDscortinas):
    idcuarto=idcuarto[0]
    if int(idcuarto) not in LecturaDeSensores.keys() or KillearHilo[int(idcuarto)]==1:
        #newkill={int(idcuarto):0}
        #KillearHilo.update(newkill)
        print ("los kill son : ",KillearHilo)
        #proceso= socketio.start_background_task(leerSensoresCortina, idcuarto,OpCortina().buscarCortinasPorCuarto(int(idcuarto))) 
        
        #newprocess={int(idcuarto):proceso}
        
        #LecturaDeSensores.update(newprocess)
        print("el id del cuarto activo es: ", idcuarto," y las cortians son : ",IDscortinas)

        

def leerSensoresCortina(idCuarto,cortinas):
    #nuevo proceso es este 
    while KillearHilo[int(idCuarto)]==0:
        print ("leendo : " ,cortinas["IdCortina"])
        for x in cortinas["IdCortina"]:
            EstadoSen1='false'
            EstadoSen2='false'
            cortActual=OpCortina().buscarIdCortina(x)
            sen1=cortActual["PinSensor1"]
            sen2=cortActual["PinSensor1"]
            eventlet.sleep(1)
            OpCortina().modidificarEstadoCortina(x,'Semi')
            socketio.emit('CortinaCambio', (int(x),'Semi'))
            eventlet.sleep(1)
            print ("soketeo el 1")
            OpCortina().modidificarEstadoCortina(x,'Abierto')
            socketio.emit('CortinaCambio', (int(x),'Abierto'))
            eventlet.sleep(1)
            OpCortina().modidificarEstadoCortina(x,'Cerrado')
            socketio.emit('CortinaCambio', (int(x),'Cerrado'))
    
@socketio.on("Stop_Lec")
def DejarDeLeerSens(idcuarto):
    print ("entraste id cuarto es" ,idcuarto)
    idcuarto=int(idcuarto)
    if idcuarto in LecturaDeSensores.keys():
        # LecturaDeSensores[idcuarto].stop()
        del LecturaDeSensores[idcuarto]
        # print ("levturas :",LecturaDeSensores)
        newkill={idcuarto:1}
        KillearHilo.update(newkill)
    else:
        print ("keys :",LecturaDeSensores.keys())
######################################################SON WEBADAS CHOCO ESTO ES PARA EL PRIMER INTENTO DE PROYECTO >v #######################################################################################
@socketio.on('luz')                                                                                                                     #
def hacer(accion):                                                                                                                      #

    global encendiendo
    if accion=='Encender':
        
        #Gpio Hihg
        luza=open('estado_luz.txt','w')
        luza.write('Encendido')
        luza.close()
        estado='Encendido'
        emit('id','Encendido',broadcast=True)
        encendiendo='1'
        
    if accion=='Apagar':
        #gPIOLOW
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
                                                                                                                                        #
''' var=accion                                                                                                                          #
    tpool.execute(encenderLuz,'1',var)'''
    # o tambien
    #    socketio.start_background_task(target=encenderLuz, ('1',var))                                                                      #
#                                                                                                                                       #
'''hiloluz=threading.Thread(target=encenderLuz('1','var'))                                                                              #
    hiloluz.start()
    
    hiloluz.join()'''
def encenderLuz(numero, estado):                                                                                                        #
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

                                                                                                                                        #
#                                                                                                                                       #
#                                                                                                                                       #
leeyendo='1'                                                                                                                            #
#                                                                                                                                       #
#                                                                                                                                       #
def abrirtextocortina():                                                                                                                #
      cor=open('estado_cortina.txt','r')
      estado=cor.read()
      cor.close()
      return estado
#                                                                                                                                       #
@socketio.on('parar')                                                                                                                   #
def parar():                                                                                                                            #
    global leeyendo
    leeyendo='0'
#                                                                                                                                       #
#                                                                                                                                       #
@socketio.on('cortina')                                                                                                                 #
def hacercortina(click,accionCortina):                                                                                                  #
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
                    print ('subiendo poco  a poco')
                    
                    

            if accionCortina=='bajando':
                estado=abrirtextocortina()
                if estado!='Cerrado':           
                    print("bajando poco a poco")

            if accionCortina=='abriendo':
                while True:
                    estado=abrirtextocortina()
                    if (estado!="Abierto" and accionCortina=="abriendo"):           
                     print("Abriendo totalemtne  :" + accionCortina )
                    else:
                         break
                
            if accionCortina=='cerrando':
                print('cerrando completamente')
                while True:
                    estado=abrirtextocortina()
                    if (estado!="Cerrado" and accionCortina=="cerrando"):           
                     print("cerrando totalemtne  :" + accionCortina )
                    else:
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
def leersensores(id):                                                                                                                   #
    global leeyendo
    tocasabajo=11
    tocasarriba=11
    while (leeyendo=='1'):
        if(leeyendo=='1'):
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
######################################################SON WEBADAS CHOCO ESTO ES PARA EL PRIMER INTENTO DE PROYECTO >v #######################################################################################    



if __name__ == '__main__':
    
    #app.run(debug=True , host= '0.0.0.0', threaded=True)
    socketio.run(app,debug=True,host='0.0.0.0')
    tpool.killall()
    #

 