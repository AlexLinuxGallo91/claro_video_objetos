from src.validaciones.imagenes import ValidacionesImagenes
from src.validaciones.series import ValidacionesSeries

class Proceso:

    @staticmethod
    def validateProcess(superhighlights):
        highlights = ValidacionesImagenes.validateUrlImage(superhighlights)
        return ValidacionesSeries.validateSequence(highlights)