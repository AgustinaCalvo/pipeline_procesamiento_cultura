import requests
from datetime import datetime
from pathlib import Path
from pipeline.config import logger


def descargar_archivos(datos_dict):
    """Descarga los archivos museos, bibliotecas y cines, de la pagina datos.gob.ar y los guarda en el disco


    Parameters
    ----------
    datos_dict : dict
        Diccionario con las url de museos, bibliotecas y cines
        Ejemplo:
            DATOS_CULTURA_URL = {
                "museos": URL_MUSEOS,
                "bibliotecas": URL_BIBLIOTECAS,
                "cines": URL_CINES,
            }

    Returns
    dict_path_archivos : dict
        Diccionario con los path de los archivos: museos, bibliotecas y cines
        Ejemplo:
            {'museos': 'data/museos/2022-07/museos-19-07-2022.csv',
            'bibliotecas': 'data/bibliotecas/2022-07/bibliotecas-19-07-2022.csv',
            'cines': 'data/cines/2022-07/cines-19-07-2022.csv'}
    """

    dict_path_archivos = {}
    for nombre, url in datos_dict.items():
        logger.info(f"Descargando archivo {nombre} desde {url}")
        r = requests.get(url, allow_redirects=True)
        date = datetime.now().strftime("%d-%m-%Y")
        year = datetime.now().strftime("%Y-%m")

        p = Path(f"./data/{nombre}/{year}")
        p.mkdir(parents=True, exist_ok=True)

        path_destino = p / f"{nombre}-{date}.csv"
        with (path_destino).open("wb") as file:
            file.write(r.content)

        logger.info(f"Archivo {nombre} descargado en {path_destino}")

        dict_path_archivos[nombre] = path_destino

    logger.info(print(dict_path_archivos))
    return dict_path_archivos
