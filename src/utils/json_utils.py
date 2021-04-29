import src.constantes.argumentos_constantes as const
from typing import Dict
import random

class JsonUtils:

    @staticmethod
    def generar_json_result_base(json_result:Dict):
        json_nodo = {}
        json_nodo['superhighlight'] = json_result['superhighlight']
        json_nodo['region'] = json_result['region']
        json_nodo['status'] = const.CONST_SUCCESS
        json_nodo['errors'] = []

        # se itera sobre cada una de las series obtenidas en el JSON
        for serie in json_result['response']:
            json_serie = JsonUtils.generar_json_result_serie(serie)
            json_nodo['errors'].append(json_serie)

        # verifica que ambas lista de errores (imagenes y secuencias) tengan al menos un elemento, en caso contrario
        # el estatus sera SUCCESS, esto debido a que no encontro ningun error en ambas listas, en caso contrario
        # el estatus sera FAILED
        json_nodo = JsonUtils.verificar_status_general_serie(json_nodo)

        return json_nodo

    @staticmethod
    def verificar_status_general_serie(json_nodo:Dict):

        for json_error in json_nodo['errors']:
            len_images = len(json_error['images'])
            len_sequences = len(json_error['sequences'])

            if len_images < 1 and len_sequences < 1:
                json_error['status'] = const.CONST_SUCCESS
            else:
                json_error['status'] = const.CONST_FAILED
                json_nodo['status'] = const.CONST_FAILED

            if len_images < 1:
                del json_error['images']

            if len_sequences < 1:
                del json_error['sequences']

        return  json_nodo

    @staticmethod
    def generar_json_result_serie(json_result_serie:Dict):
        json_serie = {}
        json_serie['status'] = const.CONST_SUCCESS
        json_serie['title'] = json_result_serie['title']
        json_serie['group_id'] = json_result_serie['group_id']
        json_serie['category'] = json_result_serie['category']
        json_serie['images'] = []
        json_serie['sequences'] = []

        # se realiza las validaciones de las imagenes de las series, en caso de que alguna imagen tenga error o
        # no responda correctamente, se adjuntara a la lista de imagenes con errores
        for key_image, value_image in json_result_serie['images'].items():
            request = value_image['request']
            verifyImage = value_image['verifyImage']

            if const.CONST_MODO_DEBUG:
                request = random.choice(const.CONST_DEBUG_LISTA_STATUS)
                verifyImage = random.choice(const.CONST_DEBUG_LISTA_STATUS)

            if request != const.CONST_SUCCESS or verifyImage != const.CONST_SUCCESS:
                json_imagen_corrupta = {}
                json_imagen_corrupta['image'] = key_image
                json_imagen_corrupta['image_url'] = value_image['image']
                json_imagen_corrupta['msg'] = const.MSG_ERROR_IMAGEN
                json_serie['images'].append(json_imagen_corrupta)

        # se realiza las validaciones de las secuencias de capitulos en cada una de las series, en caso de
        # presentarse una discontinuidad de capitulos, se adjuntara a la lista de secuencias con errores

        if 'id_serie_ag' in json_result_serie['sequence'] and 'status' in json_result_serie['sequence']:

            sequence_id_serie_ag = json_result_serie['sequence']['id_serie_ag']
            sequence_status = json_result_serie['sequence']['status']

            if const.CONST_MODO_DEBUG:
                sequence_status = random.choice(const.CONST_DEBUG_LISTA_STATUS)

            if sequence_status != const.CONST_SUCCESS:
                lista_secuencias = json_result_serie['sequence']['seasons']

                for secuencia in lista_secuencias:
                    order = secuencia['order']
                    status = secuencia['status']
                    not_found = secuencia['notFound']

                    if const.CONST_MODO_DEBUG:
                        status = random.choice(const.CONST_DEBUG_LISTA_STATUS)

                    if status != const.CONST_SUCCESS:
                        json_secuencia_corrupta = {}
                        json_secuencia_corrupta['order'] = order
                        json_secuencia_corrupta['status'] = const.CONST_FAILED
                        json_secuencia_corrupta['notFound'] = not_found
                        json_secuencia_corrupta['msg'] = const.MSG_ERROR_SECUENCIA

                        json_serie['sequences'].append(json_secuencia_corrupta)

        return json_serie

    @staticmethod
    def se_presentan_urls_imagenes_corruptas(json_result:Dict):

        result = False

        for nodo in json_result['response']:
            for json_error in nodo['errors']:
                if json_error['status'] != const.CONST_SUCCESS and 'images' in json_error:
                    len_image_errors = len(json_error['images'])
                    result = len_image_errors > 0
                    if result:
                        return result

        return result

    @staticmethod
    def se_presentan_secuencias_corruptas(json_result: Dict):

        result = False

        for nodo in json_result['response']:
            for json_error in nodo['errors']:

                if json_error['status'] != const.CONST_SUCCESS and 'sequences' in json_error:
                    len_sequences_errors = len(json_error['sequences'])
                    result = len_sequences_errors > 0
                    if result:
                        return result

        return result




