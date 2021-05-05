import json

from src.procesos.proceso import Proceso
from src.validaciones.series import ValidacionesSeries


#!/usr/bin/python
# -*- coding: utf-8 -*-

#############################################################################################################################
# Nombre: Gerardo Treviño Montelongo                                                                                        #
# Clase: validateProcess.py                                                                                                 #
# Fecha: 29/03/2021                                                                                                         #
# Correo: gerardo.trevino@triara.com                                                                                        #
# Version 1.00                                                                                                              #
# Sistema: Linux                                                                                                            #
#                                                                                                                           #
#                                                                                                                           #
# Se procesa la sista de superhighlights, se valida que la url de la imagen retorne un codigo 200 y se                      #
# realiza una validacion de la imagen para informar si esta corrupta, se realiza una validacion de las                      #
# series para comprobar que la secuencia de las temporadas y sus capitulos esten en orden y completos.                      #
#                                                                                                                           #
#                                                                                                                           #
# --- Comparar dos imagenes ---                                                                                             #
# https://programacionpython80889555.wordpress.com/2019/10/01/comparacion-de-imagenes-en-python-con-opencv-y-numpy/         #
# https://qastack.mx/programming/189943/how-can-i-quantify-difference-between-two-images                                    #
# https://qastack.mx/programming/11541154/how-can-i-assess-how-similar-two-images-are-with-opencv                           #
# https://www.it-swarm-es.com/es/python/algoritmo-de-comparacion-de-imagenes/968567672/                                     #
# https://www.it-swarm-es.com/es/image-processing/metodo-simple-y-rapido-para-comparar-imagenes-por-similitud./970353929/   #
# https://www.javaer101.com/es/article/3426818.html                                                                         #
#                                                                                                                           #
#                                                                                                                           #
#############################################################################################################################

class Main:

    # -------------------------
    # Funcion principal.
    # -------------------------s
    @staticmethod
    def main():
        # Datos iniciales del superhighlight
        superhighlights = ValidacionesSeries.jsonSuperhighlight(ValidacionesSeries.getParams())
        # Filtra las categorias para mostrar las que se necesitan. 0 = Ninguno, 1 = Series, 2 = Peliculas, 3 = Otros
        superhighlights['superhighlights']['response'] = [x for x in superhighlights['superhighlights']['response'] if
                                                          int(x['category']) in [0,1,2,3]]
        # Inicia las pruebas de validacion.
        result = Proceso.validateProcess(superhighlights)
        # Convierte el resultado en salida JSON
        dict_json = json.dumps(result['superhighlights'], indent = 4)

        return dict_json
