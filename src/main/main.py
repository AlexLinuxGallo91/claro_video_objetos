import json

from src.procesos.proceso import Proceso
from src.validaciones.series import ValidacionesSeries
from src.utils.json_utils import JsonUtils
from src.utils.html_utils import HtmlUtils
from src.utils.mail_utils import MailUtils
import src.constantes.argumentos_constantes as const
import sys

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
        # superhighlights = ValidacionesSeries.jsonSuperhighlight(ValidacionesSeries.getParams())
        # # Filtra las categorias para mostrar las que se necesitan. 0 = Ninguno, 1 = Series, 2 = Peliculas, 3 = Otros
        # superhighlights['superhighlights']['response'] = [x for x in superhighlights['superhighlights']['response'] if
        #                                                   int(x['category']) in [0,1,2,3]]
        # # Inicia las pruebas de validacion.
        # result = Proceso.validateProcess(superhighlights)
        # # Convierte el resultado en salida JSON
        # dict_json = json.dumps(result['superhighlights'], indent = 4)

        #return dict_json

        return ValidacionesSeries.getParams()


if __name__ == '__main__':
    const.CONST_MODO_DEBUG = True

    if len(sys.argv) < 2:
        print('favor de establecer la region a probar.')
        sys.exit(1)
    else:
        const.ARG_REGION = sys.argv[1]

    lista_result_response = []
    lista_correos_destinatarios = [
        'alexis.araujo@triara.com',
        'jose.hernandez@triara.com',
        'gerardo.trevino@triara.com'
        #'angel.galindo@triara.com',
        #'ernesto.contreras@triara.com'
    ]

    #se itera en cada uno de los nodos
    for nodo in const.LISTA_NODOS:
        const.ARG_SUPERHIGHLIGHT = nodo

        try:
            response = Main.main()
            json_response_obtenido = json.loads(response)
            json_response_obtenido = JsonUtils.generar_json_result_base(json_response_obtenido)
            lista_result_response.append(json_response_obtenido)
        except ValueError:
            pass
        except TypeError:
            pass

    json_result = {}
    json_result['response'] = lista_result_response
    json_result_texto = json.dumps(json_result, indent=4)

    if JsonUtils.se_presentan_urls_imagenes_corruptas(json_result):
        HTML = HtmlUtils.generar_html_table_errores_imagenes(json_result)

    if JsonUtils.se_presentan_secuencias_corruptas(json_result):
        HTML = HtmlUtils.generar_html_table_errores_secuencias(json_result)

    # valida si existen imagenes corruptas, en caso de ser asi se forma una tabla HTML para su notificacion por correo
    if JsonUtils.se_presentan_urls_imagenes_corruptas(json_result):
        HTML = HtmlUtils.generar_html_table_errores_imagenes(json_result)
        subject = MailUtils.subject_imagenes_dinamico(json_result)
        resp = MailUtils.enviar_correo(lista_correos_destinatarios, 'notificacion.itoc@triara.com',subject, HTML)
        print(resp.text)

    if JsonUtils.se_presentan_secuencias_corruptas(json_result):
        subject = MailUtils.subject_sequences_dinamico(json_result)
        HTML = HtmlUtils.generar_html_table_errores_secuencias(json_result)
        resp = MailUtils.enviar_correo(lista_correos_destinatarios, 'notificacion.itoc@triara.com', subject, HTML)
        print(resp.text)