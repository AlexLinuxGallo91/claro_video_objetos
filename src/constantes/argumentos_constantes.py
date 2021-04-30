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

LISTA_HEADERS_IMAGES = ['Super Destacado', 'Region', 'Imagen', 'Titulo', 'group_id']
LISTA_HEADERS_SEQUENCES = ['Super Destacado', 'Region', 'Orden', 'Titulo', 'group_id']

# HTML
HTML_TABLE = '<table style="{}">{}</table>'
HTML_TABLE_TR = '<tr style="{}">{}</tr>'
HTML_TABLE_TH = '<th style="{}">{}</th>'
HTML_TABLE_TD = '<td style="{}">{}</td>'

SUBJECT_SEQUENCES = 'Notificación de discontinuidad en Series en Super Destacado: {} de la región {}.'
SUBJECT_IMAGES = 'Notificación de inconcistencia en imágenes del Super Destacado: {} de la región {}.'

# HTML STYLEs
HTML_STYLE_BORDER_TABLE = 'border: 1px dotted black; border-collapse: collapse;'
HTML_STYLE_HEADER = 'border: 1px dotted black; border-collapse: collapse; background: #DEEAF6;'