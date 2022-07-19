import requests
from datetime import datetime
from pathlib import Path
from pipeline.config import logger


def descargar_archivos(datos_dict):
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

    return dict_path_archivos
