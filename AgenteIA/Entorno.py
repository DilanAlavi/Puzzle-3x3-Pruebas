#################################################################
# Nombre      : Entorno                                         #
# Version     : 0.05.03.2017                                    #
# Autor       : Victor                                          #
# Descripcion : Clase abstracta para modelar entorno            #
##################################################################

from AgenteIA.Agente import Agente


class Entorno(object):

    def __init__(self):
        self.objetos = []
        self.agentes = []

    def percibir(self, agente):
        raise Exception("Se debe implementar la captura de percepciones")

    def ejecutar(self, agente):
        raise Exception("Se debe implementar ejecutar")

    def finalizado(self):
        return any(not agente.vive for agente in self.agentes)

    def avanzar(self):

        if not self.finalizado():
            for agente in self.agentes:
                self.percibir(agente)
                self.ejecutar(agente)

    def run(self):

        while True:
            if self.finalizado():
                break
            self.avanzar()

    def insertar_objeto(self, cosa):


        assert cosa not in self.objetos, "no insertar el mismo objeto"
        self.objetos.append(cosa)
        if isinstance(cosa, Agente):
            cosa.performance = 0
            self.agentes.append(cosa)
