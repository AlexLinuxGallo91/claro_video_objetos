import json
import sys

from python3_gearman import GearmanClient

from src.utils.json_utils import JsonUtils
from src.utils.worker_utils import WorkerUtils

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

for completed_job_request in completed_requests:
        result = completed_job_request.result

        try:
            data = json.loads(result)
            lista_result_response.append(JsonUtils.generar_json_result_base(data))
        except ValueError:
            pass

        contador_errores+=1

json_result = {}
json_result['response'] = lista_result_response

print('{}\n'.format(json.dumps(json_result, indent = 4)))

