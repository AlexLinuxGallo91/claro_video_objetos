import concurrent.futures as futures
import requests
from bs4 import BeautifulSoup
import pandas as pd
import src.constantes.argumentos_constantes as const

from src.peticiones.peticiones import Peticiones


class ValidacionesSeries:

    # -------------------------------------------------------
    # Valida la continuidad de los capitulos de la serie. ---
    # -------------------------------------------------------
    @staticmethod
    def sequence(unique):
        data = {}
        data['seasons'] = []
        # Temporadas totales
        temps = int(unique[0]['Temps.']) + 1
        # Recorrer cada temporada, genera una lista con las temporadas de 1...n
        for temp in range(1, temps):
            # Obtiene la lista por temporada
            tempDict = [x for x in unique if int(x['Orden Temporada']) == temp]
            # Episodio total por temporada.
            # episodes = int(tempDict[0]['EPISODES'])
            # lenEpisodes = len(tempDict)
            lastEpisodes = int((tempDict[-1])['Orden Capitulo']) + 1  # Se agrega uno para compeltar la secuencia
            # Se genera la lista con la secuencia de numeros.
            listNumber = list(range(1, lastEpisodes))
            # Listado de episodios del API
            listEpisodes = []
            for episodie in tempDict:
                listEpisodes.append(int(episodie['Orden Capitulo']))
            # Valida cual no esta en la lista de consecutivos.
            notFound = [x for x in listNumber if x not in listEpisodes]
            resultEpisodes = {
                'order': episodie['Orden Temporada'],
                'status': ('SUCCESS' if not notFound else 'FAIL'),
                'notFound': ', '.join(map(str, notFound))
            }
            data['seasons'].append(resultEpisodes)

        return data

    # -------------------------------------
    # Buscar el ID_SERIE_AG de la serie ---
    # -------------------------------------
    @staticmethod
    def getIDAG(groupId):
        try:
            url = 'http://10.20.1.92:9200/common_clarovideo/grupo/'
            # Valida si la respuesta es SUCCESS
            response = requests.get(url + groupId)
            responseJson = response.json()
            return (responseJson['_source']['INFO_SERIE'][0]['ID_SERIE_AG'])
        except requests.exceptions.RequestException:
            return 0

    # -----------------------------------
    # Valida la secuencia de la serie ---
    # -----------------------------------
    @staticmethod
    def sequenceID(sequence):
        # Series = 1
        if int(sequence['category']) == 1:
            id_serie_ag = ValidacionesSeries.getIDAG(sequence['group_id'])
            serieValidate = ValidacionesSeries.serieSequence(Peticiones.getParams(id_serie_ag))
            # Status general para la secuencia de capitulos por temporada.
            dictStatus = [x['status'] for x in serieValidate['seasons'] if x['status'] == 'FAIL']
            status = ('FAIL' if ('FAIL' in dictStatus) else 'SUCCESS')
            sequence['sequence'] = {
                'id_serie_ag' : id_serie_ag,
                'status' : status,
                'seasons' : serieValidate['seasons']
            }
        return sequence

    # ----------------------------------------------
    # Paralelización de la secuencia de la serie ---
    # ----------------------------------------------
    @staticmethod
    def validateSequence(validateSequence):
        # print(validateSequence)
        addSequence = validateSequence['superhighlights']['response']
        # Podemos usar una declaración with para asegurarnos de que los hilos se limpien rápidamente.
        with futures.ThreadPoolExecutor(max_workers=5) as executor:
            # Inicie las operaciones de carga y marque cada futuro con su URL
            future_to_sequence = {executor.submit(
                ValidacionesSeries.sequenceID, sequence): sequence for sequence in addSequence}

            for future in futures.as_completed(future_to_sequence):
                future_to_sequence[future]

            return validateSequence

    # ------------------------------------
    # Obtiene el detalle de la serie.  ---
    # ------------------------------------

    @staticmethod
    def serieSequence(jsonParams):
        try:
            url = 'http://10.10.0.206/info_serie.php'
            # Consultar get request.
            response = requests.get(url, params=jsonParams)
            # Validar que el codigo de respuesta sea 200.
            if (response.ok):
                # Pasamos el contenido HTML de la web a un objeto BeautifulSoup()
                s = BeautifulSoup(response.content, 'html.parser').table
                # Convertir la tabla html en un diccionario (json)
                h, [_, *d] = [i.text for i in s.tr.find_all('th')], [[i.text for i in b.find_all('td')] for b in
                                                                     s.find_all('tr')]
                result = [dict(zip(h, i)) for i in d]
                # Excluir elementos duplicados
                unique = pd.DataFrame(result).drop_duplicates().to_dict('records')
                # Eliminar el ultimo elemento ya que es basura - Por una extraña razon al final sale uno en blanco
                unique.pop()
                # Valida la secuencia de la serie
                return ValidacionesSeries.sequence(unique)
                # print(unique)
        except requests.exceptions.RequestException:
            return ''

    # ---------------------------------------------------------
    #  Asignacion de categoria si es SERIE, PELICULA u OTRO ---
    # ---------------------------------------------------------
    @staticmethod
    def categoryElement(group_id, filtered_dict):
        # Si el id es null se asigna otros
        if group_id == None:
            return '3'  # Otros
        else:
            # Recorre cada valor de image para asignarle una categoria
            for filtered in filtered_dict:
                if 'SERIES' in filtered_dict[filtered]:
                    return '1'  # Series
                elif 'PELICULAS' in filtered_dict[filtered]:
                    return '2'  # Peliculas
        # Si no entra se asigna Ninguno
        return '0'  # Ninguno

    @staticmethod
    def getParams():
        # Parametros para el request.
        params = {
            'superhighlight': const.ARG_SUPERHIGHLIGHT,
            'region': const.ARG_REGION,
            'device_id': 'web',
            'device_category': 'web',
            'device_model': 'web',
            'device_type': 'web',
            'device_so': 'Chrome',
            'format': 'json',
            'device_manufacturer': 'generic',
            'authpn': 'webclient',
            'authpt': 'tfg1h3j4k6fd7',
            'api_version': 'v5.92',
            'HKS': '07qc98jp753u1e0qconlbh7uq2',
            'user_status': 'anonymous'
        }
        return params

    # ------------------------------------------
    #  Ejecuta el get para el superhighlight ---
    # ------------------------------------------
    @staticmethod
    def jsonSuperhighlight(jsonParams):
        data = {}
        #  URL para consultar.
        url = 'https://mfwkweb-api.clarovideo.net/services/cms/superhighlight'

        # Consultar get request.
        response = requests.get(url, params=jsonParams)
        # print(response.url)

        # Validar que el codigo de respuesta sea 200.
        # if (response.status_code == 200):
        if (response.ok):

            data['response'] = []
            # Se extrae el highlight del response.
            responseJson = response.json()
            if ((responseJson['response']) != None):
                highlights = responseJson['response']['highlight']
                # print(highlight)
                # Recorrer el arreglo para extraer los nodos necesarios.
                for highlight in highlights:
                    # Quitar la categoria de app_behaviour
                    if (highlight['type'] != 'app_behaviour'):
                        # Inicializar busqueda key string.
                        search_key = 'image_'
                        filtered_dict = {k: v for (k, v) in highlight.items() if (search_key in k)}
                        # Validar que no este vacio el dict.
                        if filtered_dict:
                            # JSON con los registros necesarios.
                            result = {
                                'group_id': highlight['group_id'],
                                'title': highlight['title'],
                                'images': filtered_dict,
                                'category': ValidacionesSeries.categoryElement(highlight['group_id'], filtered_dict),
                                'sequence': {}
                            }
                            data['response'].append(result)
                            # print(data)

        # Dict final con la configuracion de salida
        superhighlights = {
            'superhighlights': {
                'superhighlight': ValidacionesSeries.getParams()['superhighlight'],
                'region': ValidacionesSeries.getParams()['region'],
                'response': data['response']
            }
        }

        return (superhighlights)