import json
import sys

from python3_gearman import GearmanClient

from src.utils.mail_utils import MailUtils
from src.utils.worker_utils import WorkerUtils
from src.utils.json_utils import JsonUtils
from src.utils.html_utils import HtmlUtils
import src.constantes.argumentos_constantes as const


gm_client = GearmanClient(['localhost:4770'])

lista_constantes_imagenes = ['SUCCESS', 'FAILED']
lista_de_jobs = []
contador_errores = 0
pais_por_buscar = sys.argv[1]

# se establece una lista con los jobs a ejecutar, donde cada job contiene la region establecida y cada uno de los
# nodos
lista_de_jobs = WorkerUtils.establecer_lista_de_jobs(pais_por_buscar)

# se cargan o mandan los jobs al worker
submitted_requests = gm_client.submit_multiple_jobs(lista_de_jobs, background=False, wait_until_complete=False)

# si sobrepasa mas de 180 segundos, no regresa nada, se detiene la ejecucion del job y de resultado se obtiene un None
completed_requests = gm_client.wait_until_jobs_completed(submitted_requests, poll_timeout=180.0)

lista_result_response = []
json_error = {}
json_error['error'] = []

# DEBUG
const.CONST_MODO_DEBUG = True

for completed_job_request in completed_requests:
        result = completed_job_request.result

        try:
            json_response_obtenido = json.loads(result)
            json_response_obtenido = JsonUtils.generar_json_result_base(json_response_obtenido)
            lista_result_response.append(json_response_obtenido)
        except ValueError:
            pass

json_result = {}
json_result['response'] = lista_result_response
json_result_texto = json.dumps(json_result, indent=4)
json_result_texto = '<h3>{}</h3>'.format(json_result_texto)

# print('{}\n'.format(json_result_texto))

# valida si existen imagenes corruptas, en caso de ser asi se forma una tabla HTML para su notificacion por correo
if JsonUtils.se_presentan_urls_imagenes_corruptas(json_result):

    # se forma la tabla
    HTML = HtmlUtils.generar_html_table_errores_imagenes(json_result)

    # envio de correos
    resp = MailUtils.enviar_correo(['alexis.araujo@triara.com'], 'notificacion.itoc@triara.com',
                                   'prueba', HTML)

    print(resp.text)

if JsonUtils.se_presentan_urls_imagenes_corruptas(json_result):
    # se forma la tabla
    HTML = HtmlUtils.generar_html_table_errores_secuencias(json_result)

    # envio de correos
    resp = MailUtils.enviar_correo(['alexis.araujo@triara.com'], 'notificacion.itoc@triara.com',
                                   'prueba', HTML)

    print(resp.text)
