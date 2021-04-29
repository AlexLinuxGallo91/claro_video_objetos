import sys
import json
import random
import requests
import src.constantes.argumentos_constantes as const
from python3_gearman import GearmanClient
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
            lista_result_response.append(data)

            lista_response = data['response']
            data['errors'] = []
            data['status'] = ''

            for response in lista_response:

                lista_de_imagenes = response['images']
                lista_de_secuencias = response['sequence']
                json_image_error = {}
                json_image_error['title'] = response['title']
                json_image_error['group_id'] = response['group_id']
                json_image_error['category'] = response['category']
                json_image_error['images'] = []
                json_image_error['sequences'] = []

                for key_image, json_value in lista_de_imagenes.items():

                    #debug
                    if contador_errores < 1:
                        json_value['request'] = random.choice(lista_constantes_imagenes)
                        json_value['verifyImage'] = random.choice(lista_constantes_imagenes)

                    request = json_value['request']
                    verify_image = json_value['verifyImage']

                    if request != 'SUCCESS' or verify_image != 'SUCCESS':
                        json_imagen_fallida = {}
                        json_imagen_fallida['image'] = key_image
                        json_imagen_fallida['image_url'] = json_value['image']
                        json_imagen_fallida['msg'] = 'Imagen corrupta o no disponible'
                        json_image_error['images'].append(json_imagen_fallida)

                if len(json_image_error['images']) > 0:
                    data['errors'].append(json_image_error)

                # verifica que la secuencia tenga temporadas
                if 'id_serie_ag' in lista_de_secuencias and 'seasons' in lista_de_secuencias and 'status' in \
                        lista_de_secuencias and response['category'] == '1':

                    #debug
                    if contador_errores < 1:
                        lista_de_secuencias['status'] = random.choice(lista_constantes_imagenes)

                    if lista_de_secuencias['status'] != 'SUCCESS':
                        lista_temporadas = lista_de_secuencias['seasons']

                        for temporada in lista_temporadas:

                            #debug
                            if contador_errores < 1:
                                temporada['status'] = random.choice(lista_constantes_imagenes)

                            if temporada['status'] != 'SUCCESS':

                                json_falla_secuencia = {}
                                json_falla_secuencia['numero_de_temporada'] = temporada['order']
                                json_falla_secuencia['status'] = temporada['status']
                                json_falla_secuencia['notFound'] = temporada['notFound']
                                json_falla_secuencia['msg'] = 'Temporada con secuencia no continua de capitulos'

                                json_image_error['sequences'].append(json_falla_secuencia)

            if len(data['errors']) < 1:
                data['status'] = 'SUCCESS'
                del data['errors']
            else:
                data['status'] = 'FAILED'

            del data['response']
        except ValueError:
            pass

        contador_errores+=1

json_result = {}
json_result['response'] = lista_result_response

#print('{}\n'.format(json.dumps(json_result, indent = 4)))

region = pais_por_buscar
params = {
    "from":"notificacion.itoc@triara.com",
    "to":"jose.hernandez@triara.com,alexis.araujo@triara.com,gerardo.trevino@triara.com,angel.galindo@triara.com,"
         "ernesto.contreras@triara.com"
}

params["subject"] = "Notificacion. Reporte de errores Claro Video. Region: {}".format(region.capitalize())
params["body"]    = json.dumps(json_result, indent=3)

url = 'http://itoc-tools.triara.mexico:8083/notifications/email/html'
response = requests.post(url, data=params)

print(response.text)
