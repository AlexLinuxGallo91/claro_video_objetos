import src.constantes.argumentos_constantes as const
import json

class WorkerUtils:

    @staticmethod
    def establecer_lista_de_jobs(region:str):
        lista_de_jobs = []

        for nodo in const.LISTA_NODOS:
            data_args = {}
            data_args['region'] = region
            data_args['superhighlight'] = nodo
            data_args = json.dumps(data_args)
            lista_de_jobs.append(dict(task="test_claro_video", data=data_args))

        return lista_de_jobs

