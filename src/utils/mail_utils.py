from typing import List
import requests

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