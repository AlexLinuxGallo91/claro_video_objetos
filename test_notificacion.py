import json
import sys
import logging

import src.constantes.argumentos_constantes as const
from src.utils.html_utils import HtmlUtils
from src.utils.json_utils import JsonUtils
from src.utils.mail_utils import MailUtils
from src.main.main import Main

if __name__ == '__main__':
    const.CONST_MODO_DEBUG = True
    logger = logging.getLogger(__name__)

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
        # 'angel.galindo@triara.com',
        # 'ernesto.contreras@triara.com'
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
        logger.info(resp.text)

    if JsonUtils.se_presentan_secuencias_corruptas(json_result):
        subject = MailUtils.subject_sequences_dinamico(json_result)
        HTML = HtmlUtils.generar_html_table_errores_secuencias(json_result)
        resp = MailUtils.enviar_correo(lista_correos_destinatarios, 'notificacion.itoc@triara.com', subject, HTML)
        logger.info(resp.text)
