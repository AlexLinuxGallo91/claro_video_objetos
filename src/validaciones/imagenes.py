import concurrent.futures as futures
from src.peticiones.peticiones import Peticiones

#############################################################################################################################
# Nombre: Gerardo Treviño Montelongo                                                                                        #
# Clase: validateProcess.py                                                                                                 #
# Fecha: 29/03/2021                                                                                                         #
# Correo: gerardo.trevino@triara.com                                                                                        #
# Version 1.00                                                                                                              #
# Sistema: Linux                                                                                                            #
#                                                                                                                           #
#                                                                                                                           #
# Se procesa la sista de superhighlights, se valida que la url de la imagen retorne un codigo 200 y se                      #
# realiza una validacion de la imagen para informar si esta corrupta, se realiza una validacion de las                      #
# series para comprobar que la secuencia de las temporadas y sus capitulos esten en orden y completos.                      #
#                                                                                                                           #
#                                                                                                                           #
# --- Comparar dos imagenes ---                                                                                             #
# https://programacionpython80889555.wordpress.com/2019/10/01/comparacion-de-imagenes-en-python-con-opencv-y-numpy/         #
# https://qastack.mx/programming/189943/how-can-i-quantify-difference-between-two-images                                    #
# https://qastack.mx/programming/11541154/how-can-i-assess-how-similar-two-images-are-with-opencv                           #
# https://www.it-swarm-es.com/es/python/algoritmo-de-comparacion-de-imagenes/968567672/                                     #
# https://www.it-swarm-es.com/es/image-processing/metodo-simple-y-rapido-para-comparar-imagenes-por-similitud./970353929/   #
# https://www.javaer101.com/es/article/3426818.html                                                                         #
#                                                                                                                           #
#                                                                                                                           #
#############################################################################################################################

class ValidacionesImagenes:

    # ---------------------------------------------------------------
    # Paralelización de la revision de las imagenes con las URL`s ---
    # ---------------------------------------------------------------
    @staticmethod
    def validateUrlImage(superhighlights):
        updatehighlights = superhighlights['superhighlights']['response']
        for superhighlight in updatehighlights:
            images = superhighlight['images']
            # Podemos usar una declaración with para asegurarnos de que los hilos se limpien rápidamente.
            with futures.ThreadPoolExecutor(max_workers=5) as executor:
                # Inicie las operaciones de carga y marque cada futuro con su URL
                future_to_url = {executor.submit(Peticiones.load_url, images[url], 30): url for url in images}
                for future in futures.as_completed(future_to_url):
                    url = future_to_url[future]
                    # Json con el resultado
                    images[url] = future.result()



        return superhighlights