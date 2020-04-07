#El indexraspeberry es el  uso en la rpi lo unico que agrega o modifica es el def encender 
'''import RPi.GPIO as GPIO #Librería para controlar GPIO
GPIO.setmode(GPIO.BCM) #Simplemente nos sirve para usar números de pin de placa y no del procesador
GPIO.setwarnings(False)
led = 21 #Variable donde ponemos el pin que usaremos para el LED
GPIO.setup(led, GPIO.OUT)'''
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
from flask import Flask, render_template , request, jsonify
from flask_socketio import SocketIO , send  , emit
import threading 
import time   
import subprocess
import array
from eventlet import tpool
from Base import Cortina,Cuarto,Interruptor
from Operaciones import OpCortina,OpCuarto,OpInterruptor,Pines
from flask_cors import CORS, cross_origin
#instalar uploader filename
import os
from flask import send_file
from werkzeug.utils import secure_filename
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
app = Flask(__name__)
cont=1

global DirFondos
# UPLOAD_FOLDER ='Images/Fondos'
# UPLOAD_FOLDER= "C:\Users\gabri\Documents\Domotica Empezamos !\Prueba para tio raspberrry\Images\Fondos"
UPLOAD_FOLDER= "./Images/Fondos/"
app.config['SECRET_KEY']='secret'
app.config['UPLOAD_FOLDER']=UPLOAD_FOLDER

#tener un array de todas las luces y ese va ser dato entonces e dice en q posiciones va a haber un true o false 
def LuzEncenderApagar(posicion,cambio,array):
    #entonces aqui la posicion es al numero que queires llegar 
    print ("Enciendes este")
        


# CORS(app, sources=r'/API/*')
CORS(app, resources={r"/api/*": {"Access-Control-Allow-Origin": "*"}})
socketio=SocketIO(app)
socketio.init_app(app, cors_allowed_origins="*")

#falta en (app,async mode='threading") 
#nota sin el async mode no se puede parar el programa con cntrol c , pero si es en tiempo real !

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


##################### Cuartos###################


@app.route('/API/Cuartos')
def cuartos():
    print (OpCuarto().MostrarCuartos())
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
    #print(request.data)
    # print(request.json,"Es la reespuesta")
    # a=request.json['idcuarto']
   
    # print(request.json)
    
    #todos los json los cambiamos por forms para recivirlos mejor
    
    if request.form['idcuarto'] !='' :
        a=request.form['idcuarto']
        
        
        a=int(a)
        
       
        if  a >0 :
            errorid=0
            idscuartos=OpCuarto().MostrarCuartos()
            for i  in range (0,len (idscuartos["idcuarto"])):
                if (idscuartos['idcuarto'][i]== request.form['idcuarto']):
                    errorid=1
            
            if errorid==0:
                #print(request.form['Seleccion'] ,"este es el select ")
                if(request.form['Seleccion']=='Si'):
                    file=request.files['fondo']
                    if file and allowed_file(file.filename):
                            print("entro")
                            f = request.files['fondo']
                            concadenacion="Fondo"+request.form['nombre']+'.jpg'
                            filename=secure_filename(concadenacion)
                            f.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
                            ruta=r"C:\Users\gabri\Documents\Domotica Empezamos !\Prueba para tio raspberrry\Images\Fondos\Fondo"
                            ruta=ruta+request.form["nombre"]+".jpg"
                    return OpCuarto().insertarCuarto(request.form['idcuarto'],request.form['nombre'],ruta,request.form['contrasenha'])
                else:
                    return OpCuarto().insertarCuarto(request.form['idcuarto'],request.form['nombre'],'No',request.form['contrasenha'])

            else:
                
                return "id de cuarto utilizado"
    else:
        return "error "

@app.route('/API/Cuarto/<string:idcuarto>/del' , methods=['DELETE'])
def dele(idcuarto):
    if OpCuarto().buscaridcuarto(idcuarto)==True:
        idcuarto=int(idcuarto)

        OpCuarto().eliminarCuarto(idcuarto)
        return "eliminado satisfactoriamente"
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

        if request.form["idcuarto"]!='' and request.form["idcuarto"]!=' ':
            OpCuarto().modificarCuarto(idcuarto,"idcuarto",request.form["idcuarto"])
        if(request.form['Seleccion'])=='Si':
            print("entro a fondo")
            file=request.files['fondo']
            if file and allowed_file(file.filename):
                            print("entro")
                            f = request.files['fondo']
                            concadenacion="Fondo"+OpCuarto().MostrarCuartoEsp(idcuarto)['nombre']+'.jpg'
                            filename=secure_filename(concadenacion)
                            f.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
                            ruta=r"C:\Users\gabri\Documents\Domotica Empezamos !\Prueba para tio raspberrry\Images\Fondos\Fondo"
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
            filename=r"C:\Users\gabri\Documents\Domotica Empezamos !\Prueba para tio raspberrry\Images\Fondos\Default.png"
            return send_file(filename,mimetype='image/gif')
        else:
            filename=x["fondo"]
            return send_file(filename, mimetype='image/gif')
    else:
        return ("No existe Cuarto")
@app.route('/API/Cuarto/Fondo')
def fondodef():
    filename=r"C:\Users\gabri\Documents\Domotica Empezamos !\Prueba para tio raspberrry\Images\Fondos\Default.png"
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
            
            if request.json['Estado']== 1 or request.json['Estado']=='Encendido':
                OpInterruptor().modidificarEstadoiNT(idluz,'Encendido')
                ####funcion cambio de luz de idluz a encender
                socketio.emit('LuzCambio', (int(idluz),"Encendido"))
                
                
                tpool.execute(imprimirsi)
                # imprimirsi()
                # print ("Encendido luz ",idluz,"gracias")
                msg ="Encendido luz"  +str (idluz)+"gracias"
                return (msg)
            else:
                if request.json['Estado']== 0 or request.json['Estado']=='Apagado':
                    OpInterruptor().modidificarEstadoiNT(idluz,'Apagado')
                    imprimirsi()
                    socketio.emit('LuzCambio', (int(idluz),"Apagado"))
                    msg ="Apagando luz"  + str(idluz)+"gracias"
                    return (msg)
                else:
                    return("negativo")
        else:
            if request.method== "GET":
                a=OpInterruptor().buscarIdInterruptor(idluz)
                js=jsonify(a["Estado"])
                return js
        

            
        
    else:
        if aux==0:
            return ('NO EXISTE INTERRUPTOR')

@app.route('/API/Cuarto/<string:idcuarto>/Luz/add', methods=['POST'])
def addI(idcuarto):
    idcuarto=int(idcuarto)
    
    
    print (request.json)
    if (OpCuarto().buscaridcuarto(idcuarto)== True) :
         a=OpInterruptor().insertarInterruptor(request.json["IdInterruptor"],idcuarto,request.json["Pin"],request.json["Dimmer"],request.json["Nombre"])

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
        if aux!=0:

            if request.json["IdCuarto"] != '' and request.json["IdCuarto"] != ' ':
                OpInterruptor().modInterruptor(idLuz,"IdCuarto",request.json["IdCuarto"])
            if request.json["Pin"] != '' and request.json["Pin"] != ' ':
                OpInterruptor().modInterruptor(idLuz,"Pin",request.json["Pin"])
            if request.json["Dimmer"] != '' and request.json["Dimmer"] != ' ':
                OpInterruptor().modInterruptor(idLuz,"Dimmer",request.json["Dimmer"])
            if request.json["IdInterruptor"] != '' and request.json["IdInterruptor"] != ' ':
                OpInterruptor().modInterruptor(idLuz,"IdInterruptor",request.json["IdInterruptor"])
            if request.json["Nombre"] != '' and request.json["Nombre"] != ' ':
                OpInterruptor().modInterruptor(idLuz,"Nombre",request.json["Nombre"])
            
            return("Completado")

            
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
        print (request.json)
        b=OpCortina().insertarCortina(request.json["IdCortina"],idcuarto,request.json["Pinmotor"],request.json["PinSensor1"],request.json["PinSensor2"],request.json["Tipo"],request.json["Nombre"])
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
            if request.json["Nombre"]!='' and request.json["Nombre"]!=' ':
                OpCortina().modcortina(IdCortina,"Nombre",request.json["Nombre"])   
            if request.json["IdCuarto"]!='' and request.json["IdCuarto"]!=' ':
                OpCortina().modcortina(IdCortina,"IdCuarto",request.json["IdCuarto"])

            if request.json["Pinmotor"]!='' and request.json["Pinmotor"]!=' ':
                OpCortina().modcortina(IdCortina,"Pinmotor",request.json["Pinmotor"])
            if request.json["PinSensor1"]!='' and request.json["PinSensor1"]!=' ':
                OpCortina().modcortina(IdCortina,"PinSensor1",request.json["PinSensor1"])
            if request.json["PinSensor2"]!='' and request.json["PinSensor2"]!=' ':
                OpCortina().modcortina(IdCortina,"PinSensor2",request.json["PinSensor2"])                                
            if request.json["Tipo"]!='' and request.json["Tipo"]!=' ':
                OpCortina().modcortina(IdCortina,"Tipo",request.json["Tipo"]) 
            if request.json["IdCortina"]!='' and request.json["IdCortina"]!=' ':
                OpCortina().modcortina(IdCortina,"IdCortina",request.json["IdCortina"])   


            return "completado"

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



#####################################Pines libre ###########################
@app.route('/API/PinCor')
def PinesCor():
    pineslibres={}
    cont=0
    for x in range (1,17) :
        if Pines().BuscarPinMoto(x):
            pass
        else:
            pineslibres[cont]=x
            cont=cont+1
            
    print (pineslibres)
    return (jsonify( pineslibres))
@app.route('/API/PinSen1')
def PinesSen1():
    pineslibres={}
    cont=0
    for x in range (1,17) :
        if Pines().BuscarPinSensor1(x):
            pass
        else:
            pineslibres[cont]=x
            cont=cont+1
            
    print (pineslibres)
    return (jsonify( pineslibres))
@app.route('/API/PinSen2')
def PinesSen2():
    pineslibres={}
    cont=0
    for x in range (1,17) :
        if Pines().BuscarPinSensor2(x):
            pass
        else:
            pineslibres[cont]=x
            cont=cont+1
            
    print (pineslibres)
    return (jsonify(pineslibres))
@app.route('/API/PinInt')
def PinesInt():
    pineslibres={}
    cont=0
    for x in range (1,17) :
        if Pines().BuscarPinInt(x):
            pass
        else:
            pineslibres[cont]=x
            cont=cont+1
            
    print (pineslibres)
    return (jsonify( pineslibres))


@app.route('/API/Node/<string:ID>')
def compNode(ID):

    # search(ID)
    if int (ID)==1:
        return ("Si")
    #     mes = {"message":"yes"}
    # return(jsonify(mes))
    # return(jsonify("{message:'yes'}"))
    return ("No")

@app.route('/API/Node/<string:ID>/mqtt')
def RegNode():
    # vamos registrando 
    #     mes = {"message":"yes"}
    # return(jsonify(mes))
    # return(jsonify("{message:'yes'}"))
    return ("Si")



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

 