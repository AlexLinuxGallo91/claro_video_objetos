from src.utils.worker_utils import WorkerUtils
from src.constantes import argumentos_constantes as const
from src.main.main import Main
from src.utils.json_utils import JsonUtils
import json

# modulo para probar la funcionalidad del proyecto
jobs_list = WorkerUtils.establecer_lista_de_jobs('mexico')
list_jobs_result = []
json_final_result = {}

for job_dict in jobs_list:
    job_json_converted = json.loads(job_dict['data'])

    const.ARG_REGION = job_json_converted['region']
    const.ARG_SUPERHIGHLIGHT = job_json_converted['superhighlight']
    resp = json.loads(Main.main())
    resp = JsonUtils.generar_json_result_base(resp)
    list_jobs_result.append(resp)

json_final_result['response'] = list_jobs_result

if JsonUtils.se_presentan_secuencias_corruptas(json_final_result):
    print('se localizaron algunas secuencias corruptas')

if JsonUtils.se_presentan_urls_imagenes_corruptas(json_final_result):
    print('se localizaron algunas imagenes corruptas')





