from decouple import config
import logging


LOG_LEVEL = config("LOG_LEVEL", default="INFO")
DATABASE_URL = config("DATABASE_URL")
URL_MUSEOS = config(
    "URL_MUSEOS",
    default="https://datos.cultura.gob.ar/dataset/37305de4-3cce-4d4b-9d9a-fec3ca61d09f/resource/4207def0-2ff7-41d5-9095-d42ae8207a5d/download/museos_datosabiertos.csv",
)
URL_BIBLIOTECAS = config(
    "URL_BIBLIOTECAS",
    default="https://datos.cultura.gob.ar/dataset/37305de4-3cce-4d4b-9d9a-fec3ca61d09f/resource/01c6c048-dbeb-44e0-8efa-6944f73715d7/download/biblioteca_popular.csv",
)
URL_CINES = config(
    "URL_CINES",
    default="https://datos.cultura.gob.ar/dataset/37305de4-3cce-4d4b-9d9a-fec3ca61d09f/resource/392ce1a8-ef11-4776-b280-6f1c7fae16ae/download/cine.csv",
)


logger = logging
logger.basicConfig(level=LOG_LEVEL)
