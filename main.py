from pipeline.descarga import descargar_archivos
from pipeline.procesar_archivos import procesar_archivos
from pipeline.config import URL_MUSEOS, URL_BIBLIOTECAS, URL_CINES
from pipeline.config import logger


if __name__ == "__main__":

    DATOS_CULTURA_URL = {
        "museos": URL_MUSEOS,
        "bibliotecas": URL_BIBLIOTECAS,
        "cines": URL_CINES,
    }

    rutas_archivos_dict = descargar_archivos(DATOS_CULTURA_URL)

    procesar_archivos(rutas_archivos_dict)
