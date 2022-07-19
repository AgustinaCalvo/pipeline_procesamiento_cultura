from pipeline.descarga import descargar_archivos
from pipeline.procesar_archivos import procesar_archivos
import logging

logging.basicConfig(level=logging.INFO)


if __name__ == "__main__":
    logging.info("Descargando archivos")
    DATOS_CULTURA_URL = {
        "museos": "https://datos.cultura.gob.ar/dataset/37305de4-3cce-4d4b-9d9a-fec3ca61d09f/resource/4207def0-2ff7-41d5-9095-d42ae8207a5d/download/museos_datosabiertos.csv",
        "bibliotecas": "https://datos.cultura.gob.ar/dataset/37305de4-3cce-4d4b-9d9a-fec3ca61d09f/resource/01c6c048-dbeb-44e0-8efa-6944f73715d7/download/biblioteca_popular.csv",
        "cines": "https://datos.cultura.gob.ar/dataset/37305de4-3cce-4d4b-9d9a-fec3ca61d09f/resource/392ce1a8-ef11-4776-b280-6f1c7fae16ae/download/cine.csv",
    }
    rutas_archivos_dict = descargar_archivos(DATOS_CULTURA_URL)

    procesar_archivos(rutas_archivos_dict)