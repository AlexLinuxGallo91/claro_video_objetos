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

from urllib.request import urlopen

# import requests module.
import requests
from PIL import Image


class Peticiones:

    # ------------------------------------------------------
    # Parametros para enviar a la url del superhighlight ---
    # ------------------------------------------------------
    @staticmethod
    def getParams(idSerieAG):
        # Parametros para el request.
        params = {
                    'entorno' : 'prod',
                    'id_instalacion' : '8140',
                    'id_serie_ag' : idSerieAG,
                    'titulo' : '',
                    'estado' : '',
                    'action' : 'submitted',
                    'submit' : 'submit'
                }
        return params

    # ------------------------------------------------------------
    # Recupere una sola página e informe la URL y el contenido ---
    # ------------------------------------------------------------
    @staticmethod
    def load_url(url, timeout):
        verify = 'FAIL'
        request = 'FAIL'
        try:
            with requests.get(url, timeout=timeout) as conn:
                request = ('SUCCESS' if conn.ok else 'FAIL')
                try:
                    img = Image.open(urlopen(url))  # open the image file
                    img.verify()  # verify that it is, in fact an image
                    verify = 'SUCCESS'
                except (IOError, SyntaxError) as e:
                    print(e)
        except requests.exceptions.RequestException as e:
            print(e)

        # Result final
        verifyImage = {
            'request': request,
            'verifyImage': verify,
            'image': url
        }

        return verifyImage