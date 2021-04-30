import src.constantes.argumentos_constantes as const

class HtmlUtils:

    @staticmethod
    def generar_html_table_headers_imagenes():
        header_html = ''

        for header in const.LISTA_HEADERS_IMAGES:
            header_html+=const.HTML_TABLE_TH.format(const.HTML_STYLE_HEADER, header)

        header_html = const.HTML_TABLE_TR.format('', header_html)

        return header_html

    @staticmethod
    def generar_html_table_headers_sequences():
        header_html = ''

        for header in const.LISTA_HEADERS_SEQUENCES:
            header_html += const.HTML_TABLE_TH.format(const.HTML_STYLE_HEADER, header)

        header_html = const.HTML_TABLE_TR.format('', header_html)

        return header_html

    @staticmethod
    def generar_html_table_errores_imagenes(json_result):
        html_body = ''
        html_headers = HtmlUtils.generar_html_table_headers_imagenes()

        for nodo in json_result['response']:

            superhighlight = nodo['superhighlight']
            region = nodo['region']

            if nodo['status'] != const.CONST_SUCCESS and len(nodo['errors']) > 0:
                for nodo_error in nodo['errors']:

                    title = nodo_error['title']
                    group_id = nodo_error['group_id']

                    if 'images' in nodo_error:
                        for json_image in nodo_error['images']:
                            image = json_image['image']

                            cadena_td_html=const.HTML_TABLE_TD.format(const.HTML_STYLE_BORDER_TABLE, superhighlight)
                            cadena_td_html+=const.HTML_TABLE_TD.format(const.HTML_STYLE_BORDER_TABLE, image)
                            cadena_td_html += const.HTML_TABLE_TD.format(const.HTML_STYLE_BORDER_TABLE, title)
                            cadena_td_html += const.HTML_TABLE_TD.format(const.HTML_STYLE_BORDER_TABLE, group_id)
                            cadena_td_html=const.HTML_TABLE_TR.format(const.HTML_STYLE_BORDER_TABLE, cadena_td_html)

                            html_body+=cadena_td_html

        html_body = html_headers+html_body
        html_body = const.HTML_TABLE.format(const.HTML_STYLE_BORDER_TABLE, html_body)

        return html_body

    @staticmethod
    def generar_html_table_errores_secuencias(json_result):
        html_body = ''
        html_headers = HtmlUtils.generar_html_table_headers_sequences()

        for nodo in json_result['response']:

            superhighlight = nodo['superhighlight']
            region = nodo['region']

            if nodo['status'] != const.CONST_SUCCESS and len(nodo['errors']) > 0:
                for nodo_error in nodo['errors']:

                    title = nodo_error['title']
                    group_id = nodo_error['group_id']

                    if 'sequences' in nodo_error:
                        for json_sequence in nodo_error['sequences']:
                            order = json_sequence['order']
                            capitulos = json_sequence['notFound']

                            cadena_td_html=const.HTML_TABLE_TD.format(const.HTML_STYLE_BORDER_TABLE, superhighlight)
                            cadena_td_html+=const.HTML_TABLE_TD.format(const.HTML_STYLE_BORDER_TABLE, order)
                            cadena_td_html+=const.HTML_TABLE_TD.format(const.HTML_STYLE_BORDER_TABLE, capitulos)
                            cadena_td_html+=const.HTML_TABLE_TD.format(const.HTML_STYLE_BORDER_TABLE, title)
                            cadena_td_html+=const.HTML_TABLE_TD.format(const.HTML_STYLE_BORDER_TABLE, group_id)
                            cadena_td_html=const.HTML_TABLE_TR.format(const.HTML_STYLE_BORDER_TABLE, cadena_td_html)

                            html_body+=cadena_td_html

        html_body = html_headers+html_body
        html_body = const.HTML_TABLE.format(const.HTML_STYLE_BORDER_TABLE, html_body)

        return html_body