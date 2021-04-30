from typing import List, Dict
import requests
import src.constantes.argumentos_constantes as const

class MailUtils:

    @staticmethod
    def enviar_correo(lista_destinatarios:List, p_from, subject, body):
        url_api_correo = 'http://itoc-tools.triara.mexico:8083/notifications/email/html'

        data = {}
        data['from'] = p_from
        data['to'] = ','.join(lista_destinatarios)
        data['subject'] = subject
        data['body'] = body

        response = requests.post(url_api_correo, data=data)

        return response

    @staticmethod
    def subject_sequences_dinamico(json_result_sequences:Dict):
        region = ''
        lista_nodos_afectados = []

        for json_nodo in json_result_sequences['response']:
            region = json_nodo['region']
            if json_nodo['status'] != const.CONST_SUCCESS:
                for json_error in json_nodo['errors']:
                    if 'sequences' in json_error:
                        lista_nodos_afectados.append(json_nodo['superhighlight'])
                        break

        lista_nodos_afectados = list(dict.fromkeys(lista_nodos_afectados))

        return const.SUBJECT_SEQUENCES.format(', '.join(lista_nodos_afectados), region)

    @staticmethod
    def subject_imagenes_dinamico(json_result_sequences: Dict):
        region = ''
        lista_nodos_afectados = []

        for json_nodo in json_result_sequences['response']:
            region = json_nodo['region']
            if json_nodo['status'] != const.CONST_SUCCESS:
                for json_error in json_nodo['errors']:
                    if 'images' in json_error:
                        lista_nodos_afectados.append(json_nodo['superhighlight'])
                        break

        lista_nodos_afectados = list(dict.fromkeys(lista_nodos_afectados))

        return const.SUBJECT_SEQUENCES.format(', '.join(lista_nodos_afectados), region)

