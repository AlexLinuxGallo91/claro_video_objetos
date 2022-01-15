from os import path
from pathlib import Path as path_parent

ARG_REGION = ''
ARG_SUPERHIGHLIGHT = ''

RESPONSE_ERROR = {'error':True,'msg':''}
LISTA_NODOS = ['homeuser', 'catalogo', 'renta', 'ninios', 'hbo', 'playngo', 'Paramount', 'atresplayer']

CONST_SUCCESS = 'SUCCESS'
CONST_FAILED = 'FAILED'

MSG_ERROR_IMAGEN = 'Imagen corrupta o no disponible'
MSG_ERROR_SECUENCIA = 'Temporada con secuencia no continua de capitulos'

# DEBUG
CONST_MODO_DEBUG = False
CONST_DEBUG_LISTA_STATUS = [CONST_FAILED, CONST_SUCCESS]

HEADER_GROUP_ID = 'group_id'
HEADER_IMAGE = 'image'
HEADER_SUPERHIGHLIGHT = 'superhighlight'
HEADER_REGION = 'region'

LISTA_HEADERS_IMAGES = ['Super Destacado', 'Imagen', 'Titulo', 'group_id']
LISTA_HEADERS_SEQUENCES = ['Super Destacado', 'Temporada', 'Capitulos' ,'Titulo Serie', 'group_id', 'id_serie_ag']

# HTML
HTML_MSG_NOTIFICACION_IMAGES = '<p>Se notifica una inconsistencia de imágenes, detectada en el monitoreo interno de ' \
                               'Triara del Servicio de Claro Video:</p><br>'

HTML_MSG_NOTIFICACION_SEQUENCES= '<p>Se notifica una inconsistencia de episodios en las series detalladas, detectada ' \
                                 'en el monitoreo interno de Triara del Servicio de Claro Video:</p><br>'

HTML_TABLE = '<table style="{}">{}</table>'
HTML_TABLE_TR = '<tr style="{}">{}</tr>'
HTML_TABLE_TH = '<th style="{}">{}</th>'
HTML_TABLE_TD = '<td style="{}">{}</td>'
HTML_HREF = '<a href="{}">{}</a>'

SUBJECT_SEQUENCES = 'Notificación de discontinuidad en Series en Super Destacado: {} de la región {}.'
SUBJECT_IMAGES = 'Notificación de inconsistencia en imágenes del Super Destacado: {} de la región {}.'

# HTML STYLEs
HTML_STYLE_BORDER_TABLE = 'border: 1px dotted black; border-collapse: collapse; padding: 5px;'
HTML_STYLE_HEADER = 'border: 1px dotted black; border-collapse: collapse; background: #DEEAF6; padding: 5px;'

CONF_ROOT_DIR_PROJECT = path_parent(path.abspath(__file__)).parent.parent.parent
LOG_FORMAT = '%(asctime)s :: %(levelname)s: %(message)s'
