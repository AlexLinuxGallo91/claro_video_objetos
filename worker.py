import json

from python3_gearman import GearmanWorker

import src.constantes.argumentos_constantes as const
from src.main.main import Main

######################################################################################
##                        WORKER PYTHON GEARMAN CLARO VIDEO                         ##
##                                                                                  ##
##  Modulo/Worker en python el cual realiza el test de capitulos e imagenes         ##
##  en la plataforma de Claro Video                                                 ##
######################################################################################

# se define el worker, host y puerto al que estara a la escucha de cada peticion
# para realizar un nuevo Job
host = '127.0.0.1'
puerto = '4770'
worker = GearmanWorker(['{}:{}'.format(host, puerto)])

# funcion encarga de comunicarse al modulo de experiencia de usuario OWA
# el cual como resultado se obtiene una cadena en formato JSON
def test_claro_video(gearman_worker, gearman_job):

    hubo_error = False
    msg_error = ''
    arg = gearman_job.data

    # valida que el texto sea un json
    try:
        json_arg = json.loads(arg)
    except ValueError:
        msg_error = 'El argumento no es un json valido, favor de establecer el argumento correctamente.'
        hubo_error = True

    # valida que se encuentre la regios y el nodo establecido
    if 'superhighlight' not in json_arg:
        msg_error = 'Favor de establecer el parametro superhighlight dentro del JSON'
        hubo_error = True
    elif 'region' not in json_arg:
        msg_error = 'Favor de establecer el parametro region dentro del JSON'
        hubo_error = True
    else:
        # se establecen ambos argumentos dentro de las constantes para su uso global
        const.ARG_REGION = json_arg['region']
        const.ARG_SUPERHIGHLIGHT = json_arg['superhighlight']

    try:
        response = Main.main()
    except Exception as e:
        hubo_error = True
        msg_error = 'Sucedio un error dentro de la ejecucion princial del Script: {}'.format(e)

    if hubo_error:
        const.RESPONSE_ERROR['msg'] = msg_error
        const.RESPONSE_ERROR['error'] = hubo_error
        return json.dumps(const.RESPONSE_ERROR)
    else:
        return response

worker.register_task('test_claro_video', test_claro_video)
worker.work()