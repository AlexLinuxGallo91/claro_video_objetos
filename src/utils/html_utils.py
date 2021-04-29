import src.constantes.argumentos_constantes as const

class HtmlUtils:

    @staticmethod
    def generar_html_table_headers_imagenes():
        header_html = ''

        for header in const.LISTA_HEADERS_IMAGES:
            header_html+=const.HTML_TABLE_TH.format(const.HTML_STYLE_BORDER_TABLE, header)

        header_html = const.HTML_TABLE_TR.format('', header_html)

        return header_html

    @staticmethod
    def generar_html_table_errores_imagenes(json_result):
        html_body = ''

        html_headers = HtmlUtils.generar_html_table_headers_imagenes()

        for nodo in json_result['response']:

            superhighlight = nodo['superhighlight']
            region = nodo['region']

            if 'images' in nodo:
                for json_error_image in nodo['images']:
                    image = json_error_image['image']
                    image_url = json_error_image['image_url']

                cadena_td_html=const.HTML_TABLE_TD.format(const.HTML_STYLE_BORDER_TABLE, superhighlight)
                cadena_td_html+=const.HTML_TABLE_TD.format(const.HTML_STYLE_BORDER_TABLE, region)
                cadena_td_html+=const.HTML_TABLE_TD.format(const.HTML_STYLE_BORDER_TABLE, image)
                cadena_td_html+=const.HTML_TABLE_TD.format(const.HTML_STYLE_BORDER_TABLE, image_url)
                cadena_td_html=const.HTML_TABLE_TR.format(const.HTML_STYLE_BORDER_TABLE, cadena_td_html)

                html_body+=cadena_td_html

        html_body = html_headers+html_body
        html_body = const.HTML_TABLE.format(const.HTML_STYLE_BORDER_TABLE, html_body)

        return html_body