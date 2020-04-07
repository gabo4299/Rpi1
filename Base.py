class Cuarto:

    def __init__(self,idcuarto, nombre, fondo, contrasenha, NDispositivos):
        self.idcuarto = idcuarto
        self.nombre = nombre
        self.fondo = fondo
        self.contrasenha = contrasenha
        self.NDispositivos = NDispositivos

    def toDBCollection (self):
        return {
            "idcuarto":self.idcuarto,
            "nombre":self.nombre,
            "fondo":self.fondo,
            "contrasenha": self.contrasenha,
            "NDispositivos":self.NDispositivos
        }

    def __str__(self):
        return "idcuarto : %i - Nombre: %s - fondo: %s - contrasenha: %s  - NDispositivos: %i" \
               %(self.idcuarto, self.nombre, self.fondo, self.contrasenha,  self.NDispositivos)

class Interruptor:
    def __init__(self,IdInterruptor, IdCuarto, Pin, Dimmer, Estado,Nombre):
        self.IdInterruptor = IdInterruptor
        self.IdCuarto = IdCuarto
        self.Pin = Pin
        self.Dimmer = Dimmer
        self.Estado = Estado
        self.Nombre = Nombre


    def toDBCollection (self):
        return {
            "IdInterruptor":self.IdInterruptor,
            "IdCuarto":self.IdCuarto,
            "Pin":self.Pin,
            "Dimmer": self.Dimmer,
            
            "Estado":self.Estado,
            "Nombre":self.Nombre
        }

    def __str__(self):
        return "IdInterruptor : %i - IdCuarto: %i - Pin: %i - Dimmer: %s  - Estado: %s - Nombre: %s" \
               %(self.IdInterruptor, self.IdCuarto, self.Pin, self.Dimmer,  self.Estado, self.Nombre)

class Cortina:

    def __init__(self,IdCortina, IdCuarto, Pinmotor, PinSensor1, PinSensor2, Tipo, Estado,Nombre):
        self.IdCortina = IdCortina
        self.IdCuarto = IdCuarto
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
            "Pinmotor":self.Pinmotor,
            "PinSensor1":self.PinSensor1,
            "PinSensor2":self.PinSensor2,
            "Tipo": self.Tipo,
            
            "Estado":self.Estado,
            "Nombre":self.Nombre
        }

    def __str__(self):
        return "IdCortina : %i -IdCuarto : %i - Pinmotor: %i - PinSensor1: %s -PinSensor2: %s - Tipo: %s  - Estado: %i - Nombre: %s" \
               %(self.IdCortina, self.IdCuarto, self.Pinmotor, self.PinSensor1, self.PinSensor2, self.Tipo,  self.Estado, self.Nombre)