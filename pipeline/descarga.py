import requests
from datetime import datetime
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO)


def descargar_archivos(datos_dict):
    # TODO: Agregar mensaje de descarga y error
    dict_path_archivos = {}
    for nombre, url in datos_dict.items():
        r = requests.get(url, allow_redirects=True)
        date = datetime.now().strftime("%d-%m-%Y")
        year = datetime.now().strftime("%Y-%m")

        p = Path(f"./data/{nombre}/{year}")
        p.mkdir(parents=True, exist_ok=True)

        path_destino = p / f"{nombre}-{date}.csv"
        with (path_destino).open("wb") as file:
            file.write(r.content)

        dict_path_archivos[nombre] = path_destino

    return dict_path_archivos


# Testeo de funcionamiento de funcion

if __name__ == "__main__":
    logging.info("Descargando archivos")
    DATOS_CULTURA_URL = {
        "museos": "https://datos.cultura.gob.ar/dataset/37305de4-3cce-4d4b-9d9a-fec3ca61d09f/resource/4207def0-2ff7-41d5-9095-d42ae8207a5d/download/museos_datosabiertos.csv",
        "bibliotecas": "https://datos.cultura.gob.ar/dataset/37305de4-3cce-4d4b-9d9a-fec3ca61d09f/resource/01c6c048-dbeb-44e0-8efa-6944f73715d7/download/biblioteca_popular.csv",
        "cines": "https://datos.cultura.gob.ar/dataset/37305de4-3cce-4d4b-9d9a-fec3ca61d09f/resource/392ce1a8-ef11-4776-b280-6f1c7fae16ae/download/cine.csv",
    }
    path_archivo = descargar_archivos(DATOS_CULTURA_URL)

    print(path_archivo)