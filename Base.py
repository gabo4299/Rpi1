class Cuarto:

    def __init__(self,idcuarto,idcasa, nombre, fondo, contrasenha, NDispositivos):
        self.idcuarto = idcuarto
        self.idcasa = idcasa
        self.nombre = nombre
        self.fondo = fondo
        self.contrasenha = contrasenha
        self.NDispositivos = NDispositivos

    def toDBCollection (self):
        return {
            "idcuarto":self.idcuarto,
            "idcasa":self.idcasa,
            "nombre":self.nombre,
            "fondo":self.fondo,
            "contrasenha": self.contrasenha,
            "NDispositivos":self.NDispositivos
        }

    def __str__(self):
        return "idcuarto : %i - idcasa: %i - Nombre: %s - fondo: %s - contrasenha: %s  - NDispositivos: %i" \
               %(self.idcuarto, self.idcasa,self.nombre, self.fondo, self.contrasenha,  self.NDispositivos)

class Interruptor:
    def __init__(self,IdInterruptor, IdCuarto,IdDisp,Dispositivo, Pin, Dimmer, Estado,Nombre):
        self.IdInterruptor = IdInterruptor
        self.IdCuarto = IdCuarto
        self.IdDisp = IdDisp
        self.Dispositivo = Dispositivo
        self.Pin = Pin
        self.Dimmer = Dimmer
        self.Estado = Estado
        self.Nombre = Nombre


    def toDBCollection (self):
        return {
            "IdInterruptor":self.IdInterruptor,
            "IdCuarto":self.IdCuarto,
            "Nombre":self.Nombre,
            "IdDisp":self.IdDisp,
            "Dispositivo":self.Dispositivo,
            "Pin":self.Pin,
            "Dimmer": self.Dimmer,
            
            "Estado":self.Estado
            
            
        }

    def __str__(self):
        return "IdInterruptor : %i - IdCuarto: %i - IdDisp: %i- Dispositivo: %s- Pin: %i - Dimmer: %s  - Estado: %s - Nombre: %s" \
               %(self.IdInterruptor, self.IdCuarto,self.IdDisp,self.Dispositivo, self.Pin, self.Dimmer,  self.Estado, self.Nombre)

class Cortina:

    def __init__(self,IdCortina, IdCuarto,IdDisp,Dispositivo, Pinmotor, PinSensor1, PinSensor2, Tipo, Estado,Nombre):
        self.IdCortina = IdCortina
        self.IdCuarto = IdCuarto
        self.IdDisp = IdDisp
        self.Dispositivo = Dispositivo
        self.Pinmotor = Pinmotor
        self.PinSensor1 = PinSensor1
        self.PinSensor2 = PinSensor2
        self.Tipo = Tipo
        self.Estado = Estado
        self.Nombre=Nombre

    def toDBCollection (self):
        return {
            "IdCortina":self.IdCortina,
            "IdCuarto":self.IdCuarto,
            "IdDisp":self.IdDisp,
            "Dispositivo":self.Dispositivo,
            "Pinmotor":self.Pinmotor,
            "PinSensor1":self.PinSensor1,
            "PinSensor2":self.PinSensor2,
            "Tipo": self.Tipo,
            
            "Estado":self.Estado,
            "Nombre":self.Nombre
        }

    def __str__(self):
        return "IdCortina : %i -IdCuarto : %i - IdDisp: %i - Dispositivo: %s - Pinmotor: %i - PinSensor1: %s -PinSensor2: %s - Tipo: %s  - Estado: %i - Nombre: %s" \
               %(self.IdCortina, self.IdCuarto, self.IdDisp,self.Dispositivo,self.Pinmotor, self.PinSensor1, self.PinSensor2, self.Tipo,  self.Estado, self.Nombre)

class Raspberry:
    def __init__(self,IdRasp,IdCasa,PinesLibres,PinesOcupados,NPL,NPO,PWM, PWMLibre,Sensores,Sensoreslibres,Luz,Luzlibre,Descripcion):
        self.IdRasp = IdRasp
        self.IdCasa = IdCasa
        self.PinesLibres = PinesLibres
        self.PinesOcupados = PinesOcupados
        self.NPL=NPL
        self.NPO=NPO
        self.PWM=PWM
        self.PWMLibre=PWMLibre
        self.Sensores=Sensores
        self.Sensoreslibres=Sensoreslibres
        self.Luz=Luz
        self.Luzlibre=Luzlibre
        self.Descripcion=Descripcion
        

    def toDBCollection (self):
        return {
            "IdRasp":self.IdRasp,
            "IdCasa":self.IdCasa,
            "PinesLibres":self.PinesLibres,
            "PinesOcupados":self.PinesOcupados ,
            "Cantidad Pines Libres":self.NPL    ,
            "Cantidad Pines Ocupados":self.NPO, 
            "Cantidad PWM":self.PWM,
            "PWM Libres":self.PWMLibre,
            "Cantidad Sensores":self.Sensores,
            "Sensores Libres":self.Sensoreslibres,
            "Cantidad Interruptores/Luces":self.Luz,
            "Interruptores/Luces Libres":self.Luzlibre,
            "Descripcion":self.Descripcion

        }

    def __str__(self):
        return "IdRasp : %i -IdCasa : %i - PinesLibres: %s - PinesOcupados: %s -Cantidad Pines Libres: %i - Cantidad Pines Ocupados: %i - Cantidad PWM: %i - PWM Libres: %s - Cantidad Sensores: %i - Sensores Libres: %s - Cantidad Interruptores/Luces: %i - Interruptores/Luces Libres: %s -Descripcion: %s " \
               %(self.IdRasp, self.IdCasa, self.PinesLibres, self.PinesOcupados, self.NPL, self.NPO, self.PWM, self.PWMLibre, self.Sensores, self.Sensoreslibres, self.Luz, self.Luzlibre,self.Descripcion  )


class Node:
    def __init__(self,IdNode,IdCasa,PinesLibres,PinesOcupados,NPL,NPO,AnalogLibre,AnalogOcupado,Analog,Estado,Descripcion):
        self.IdNode = IdNode
        self.IdCasa = IdCasa
        self.PinesLibres = PinesLibres
        self.PinesOcupados = PinesOcupados
        self.NPL=NPL
        self.NPO=NPO
        self.AnalogLibre=AnalogLibre
        self.AnalogOcupado=AnalogOcupado
        self.Analog=Analog
        self.Estado=Estado
        self.Descripcion=Descripcion

        
    def toDBCollection (self):
        return {
            "IdNode":self.IdNode,
            "IdCasa":self.IdCasa,
            "PinesLibres":self.PinesLibres,
            "PinesOcupados":self.PinesOcupados ,
            "Cantidad Pines Libres":self.NPL    ,
            "Cantidad Pines Ocupados":self.NPO,
            "Analogico Libre":self.AnalogLibre,
            "Analogico Ocupado":self.AnalogOcupado,
            "Cantidad Analogicos":self.Analog,
            "Estado":self.Estado,
            "Descripcion":self.Descripcion
              
        }

    def __str__(self):
        return "IdNode : %i -IdCasa : %i - PinesLibres: %s - PinesOcupados: %s -Cantidad Pines Libres: %i - Cantidad Pines Ocupados: %i - Analogico Libre: %s - Analogico Ocupado: %s - Cantidad Analogicos: %i - Estado: %s - Descripcion: %s" \
               %(self.IdNode, self.IdCasa, self.PinesLibres, self.PinesOcupados, self.NPL, self.NPO ,self.AnalogLibre,self.AnalogOcupado,self.Analog ,self.Estado,self.Descripcion)
class Esp32:
    def __init__(self,IdEsp32,IdCasa,PinesLibres,PinesOcupados,NPL,NPO,Estado,Descripcion):
        self.IdEsp32 = IdEsp32
        self.IdCasa = IdCasa
        self.PinesLibres = PinesLibres
        self.PinesOcupados = PinesOcupados
        self.NPL=NPL
        self.NPO=NPO
        self.Estado=Estado
        self.Descripcion=Descripcion

        
    def toDBCollection (self):
        return {
            "IdEsp32":self.IdEsp32,
            "IdCasa":self.IdCasa,
            "PinesLibres":self.PinesLibres,
            "PinesOcupados":self.PinesOcupados ,
            "Cantidad Pines Libres":self.NPL    ,
            "Cantidad Pines Ocupados":self.NPO,
            "Estado":self.Estado,
            "Descripcion":self.Descripcion
              
        }

    def __str__(self):
        return "IdEsp32 : %i -IdCasa : %i - PinesLibres: %s - PinesOcupados: %s -Cantidad Pines Libres: %i - Cantidad Pines Ocupados: %i - Estado: %s -Descripcion: %s" \
               %(self.IdEsp32, self.IdCasa, self.PinesLibres, self.PinesOcupados, self.NPL, self.NPO ,self.Estado,self.Descripcion)
class Control:
    def __init__(self,Idontrol,IdDisp,Marca,Dispositivo,Pin,Nombre,IdCuarto,Codigos,Tipo):
        self.Idontrol = Idontrol
        self.IdDisp = IdDisp
        self.Marca = Marca
        self.Dispositivo = Dispositivo
        self.Pin=Pin
        self.Nombre=Nombre
        self.IdCuarto=IdCuarto
        self.Codigos=Codigos
        self.Tipo=Tipo

    def toDBCollection (self):
        return {
            "IdControl":self.Idontrol,
            "IdDisp":self.IdDisp,
            "Marca":self.Marca,
            "Dispositivo":self.Dispositivo ,
            "Pin":self.Pin ,
            "Nombre":self.Nombre,
            "IdCuarto":self.IdCuarto,
            "Codigos":self.Codigos,
            "Tipo":self.Tipo
        }

    def __str__(self):
        return "IdControl : %i -IdDisp : %i - Marca: %s - Dispositivo: %s  - Pin: %i -IdCuarto:%i -Codigos:%s   -Tipo :%s" \
               %(self.Idontrol, self.IdDisp, self.Marca, self.Dispositivo, self.Pin ,self.IdCuarto,self.Codigos,self.Tipo )

class LecIR:
    def __init__(self,IdLec,IdDisp,IdCasa,Dispositivo,Pin,LastData):
        '''Cuando Inicias a leer el codigo sera por 3 seg , ASYNCRONO y cambiaras el last data
         , habra una funcion que sera copiar el lastadata a el nevo codigo con el  nombre que vendra del front end '''
        self.IdLec = IdLec
        self.IdDisp = IdDisp
        self.IdCasa=IdCasa
        self.Dispositivo = Dispositivo
        self.Pin=Pin
        self.LastData=LastData
    def toDBCollection (self):
        return {
            "IdLec":self.IdLec,
            "IdDisp":self.IdDisp,
            "IdCasa":self.IdCasa,
            "Dispositivo":self.Dispositivo ,
            "Pin":self.Pin,
            "LastData":self.LastData
            #INCOMING DATA
        }

    def __str__(self):
        return "IdLec : %i -IdDisp : %i -IdCasa%i  - Dispositivo: %s  - Pin: %i - LastData: %s " \
               %(self.IdLec, self.IdDisp,self.IdCasa, self.Dispositivo, self.Pin ,self.LastData )

class MarcasControles:
    def __init__(self,Marca,Codigos,Sistema):
        self.Marca = Marca
        self.Codigos=Codigos
        self.Sistema=Sistema

    def toDBCollection (self):
        return {
            "Marca":self.Marca,
            "Codigos":self.Codigos,
            "Sistema":self.Sistema
        }

    def __str__(self):
        return " Marca: %s -Codigos:%s -Sistema: %s " \
               %( self.Marca, self.Codigos ,self.Sistema)

    
# class CodigosIR:
#      def __init__(self,IdCodigo,Nombre,codigo,Funcion):
#         self.IdCodigo = IdCodigo
#         self.Nombre = Nombre
#         self.codigo = codigo
#         self.Funcion=Funcion   

#      def toDBCollection (self):
#         return {
#             "IdCodigo":self.IdCodigo,
#             "Nombre":self.Nombre,
#             "codigo":self.codigo ,
#             "Funcion":self.Funcion    
#         }

#      def __str__(self):
#         return "IdCodigo : %i -Nombre : %s  - codigo: %s  - Funcion: %s  " \
#                %(self.IdCodigo, self.Nombre, self.codigo, self.Funcion  )


class Casa:

    def __init__(self,IdCasa, Nombre, Rasp, Node, NDispositivos, Ip, Ports,CantidadCuartos):
        self.IdCasa = IdCasa
        self.Nombre = Nombre
        self.Rasp = Rasp
        self.Node = Node
        self.NDispositivos = NDispositivos
        self.Ip = Ip
        self.Ports = Ports
        self.CantidadCuartos=CantidadCuartos

    def toDBCollection (self):
        return {
            "IdCasa":self.IdCasa,
            "Nombre":self.Nombre,
            "Rasp":self.Rasp,
            "Node":self.Node,
            "NDispositivos":self.NDispositivos,
            "Ip": self.Ip,
            
            "Ports":self.Ports,
            "CantidadCuartos":self.CantidadCuartos
            
        }

    def __str__(self):
        return "IdCasa : %i -Nombre : %s - Rasp: %i - Node: %i -NDispositivos: %i - Ip: %s  - Ports: %s - CantidadCuartos: %i" \
               %(self.IdCasa, self.Nombre, self.Rasp, self.Node, self.NDispositivos, self.Ip,  self.Ports,self.CantidadCuartos)