import src.constantes.argumentos_constantes as const
import html


class HtmlUtils:

    @staticmethod
    def generar_html_table_headers_imagenes():
        header_html = ''

        for header in const.LISTA_HEADERS_IMAGES:
            header_html += const.HTML_TABLE_TH.format(const.HTML_STYLE_HEADER, header)

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

            if nodo['status'] != const.CONST_SUCCESS and len(nodo['errors']) > 0:
                for nodo_error in nodo['errors']:

                    title = nodo_error['title']
                    group_id = nodo_error['group_id']
                    id_serie_ag = nodo_error['id_serie_ag']

                    if 'images' in nodo_error:
                        for json_image in nodo_error['images']:
                            image = json_image['image']
                            url = html.escape(json_image['image_url'])

                            cadena_td_html = const.HTML_TABLE_TD.format(const.HTML_STYLE_BORDER_TABLE, superhighlight)
                            cadena_td_html += const.HTML_TABLE_TD.format(const.HTML_STYLE_BORDER_TABLE,
                                                                         const.HTML_HREF.format(url, image))
                            cadena_td_html += const.HTML_TABLE_TD.format(const.HTML_STYLE_BORDER_TABLE, title)
                            cadena_td_html += const.HTML_TABLE_TD.format(const.HTML_STYLE_BORDER_TABLE, group_id)
                            cadena_td_html = const.HTML_TABLE_TR.format(const.HTML_STYLE_BORDER_TABLE, cadena_td_html)

                            html_body += cadena_td_html

        html_body = html_headers + html_body
        html_body = const.HTML_TABLE.format(const.HTML_STYLE_BORDER_TABLE, html_body)
        html_body = const.HTML_MSG_NOTIFICACION_IMAGES + html_body

        return html_body

    @staticmethod
    def generar_html_table_errores_secuencias(json_result):
        html_body = ''
        html_headers = HtmlUtils.generar_html_table_headers_sequences()

        for nodo in json_result['response']:

            superhighlight = nodo['superhighlight']

            if nodo['status'] != const.CONST_SUCCESS and len(nodo['errors']) > 0:
                for nodo_error in nodo['errors']:

                    title = nodo_error['title']
                    group_id = nodo_error['group_id']
                    id_serie_ag = nodo_error['id_serie_ag']
                    category = nodo_error['category']

                    # se consideran solo las secuencias que sean categoria 1 (sean series) y que en realidad tengan
                    # secuencias de capitulos de cada temporada
                    if 'sequences' in nodo_error and category == '1':
                        for json_sequence in nodo_error['sequences']:
                            order = json_sequence['order']
                            capitulos = json_sequence['notFound']
                            name_serie = ''

                            if 'name_serie' in nodo_error:
                                name_serie = nodo_error['name_serie']

                            cadena_td_html = const.HTML_TABLE_TD.format(const.HTML_STYLE_BORDER_TABLE, superhighlight)
                            cadena_td_html += const.HTML_TABLE_TD.format(const.HTML_STYLE_BORDER_TABLE, order)
                            cadena_td_html += const.HTML_TABLE_TD.format(const.HTML_STYLE_BORDER_TABLE, capitulos)
                            cadena_td_html += const.HTML_TABLE_TD.format(const.HTML_STYLE_BORDER_TABLE, name_serie)
                            cadena_td_html += const.HTML_TABLE_TD.format(const.HTML_STYLE_BORDER_TABLE, group_id)
                            cadena_td_html += const.HTML_TABLE_TD.format(const.HTML_STYLE_BORDER_TABLE, id_serie_ag)
                            cadena_td_html = const.HTML_TABLE_TR.format(const.HTML_STYLE_BORDER_TABLE, cadena_td_html)

                            html_body += cadena_td_html

        html_body = html_headers + html_body
        html_body = const.HTML_TABLE.format(const.HTML_STYLE_BORDER_TABLE, html_body)
        html_body = const.HTML_MSG_NOTIFICACION_SEQUENCES + html_body

        return html_body
