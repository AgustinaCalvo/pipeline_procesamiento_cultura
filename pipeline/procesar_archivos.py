import pandas as pd
import numpy as np
from sqlalchemy import create_engine, text, exc
from datetime import datetime
from pipeline.config import DATABASE_URL
from pipeline.config import logger


def procesar_archivos(dict_path):

    logger.info("Importando archivos descargados")

    museo = pd.read_csv(dict_path["museos"])
    logger.info("Importacion museos completa")

    biblioteca = pd.read_csv(dict_path["bibliotecas"])
    logger.info("Importacion bibliotecas completa")

    cine = pd.read_csv(dict_path["cines"])
    logger.info("Importacion cines completa")

    # NORMALIZACION DE DATOS DE TABLAS

    museo.columns = [
        "cod_localidad",
        "id_provincia",
        "id_departamento",
        "observaciones",
        "categoria",
        "subcategoria",
        "provincia",
        "localidad",
        "nombre",
        "domicilio",
        "piso",
        "codigo_postal",
        "cod_area",
        "telefono",
        "mail",
        "web",
        "latitud",
        "longitud",
        "tipo_latitud_longitud",
        "info_adicional",
        "fuente",
        "tipo_gestion",
        "ano_inauguracion",
        "ano_actualizacion",
    ]

    biblioteca.columns = [
        "cod_localidad",
        "id_provincia",
        "id_departamento",
        "observaciones",
        "categoria",
        "subcategoria",
        "provincia",
        "departamento",
        "localidad",
        "nombre",
        "domicilio",
        "piso",
        "codigo_postal",
        "cod_area",
        "telefono",
        "mail",
        "web",
        "info_adicional",
        "latitud",
        "longitud",
        "tipo_latitud_longitud",
        "fuente",
        "tipo_gestion",
        "ano_inauguracion",
        "ano_actualizacion",
    ]

    cine.columns = [
        "cod_localidad",
        "id_provincia",
        "id_departamento",
        "observaciones",
        "categoria",
        "provincia",
        "departamento",
        "localidad",
        "nombre",
        "domicilio",
        "piso",
        "codigo_postal",
        "cod_area",
        "telefono",
        "mail",
        "web",
        "info_adicional",
        "latitud",
        "longitud",
        "tipo_latitud_longitud",
        "fuente",
        "tipo_gestion",
        "pantallas",
        "butacas",
        "espacio_incaa",
        "ano_actualizacion",
    ]

    # Formateo de valores nulos o sin datos

    museo = museo.replace("s/d", np.nan)
    biblioteca = biblioteca.replace("s/d", np.nan)
    cine = cine.replace("s/d", np.nan)

    # Formateo de telefono y codigo de area
    museo["telefono"] = museo["telefono"].str.replace(" ", "")
    biblioteca["telefono"] = biblioteca["telefono"].str.replace(" ", "")
    cine["telefono"] = cine["telefono"].str.replace(" ", "")

    museo["cod_area"] = museo["cod_area"].astype("Int64")
    biblioteca["cod_area"] = biblioteca["cod_area"].astype("Int64")
    cine["cod_area"] = cine["cod_area"].astype("Int64")

    # Formateo de ano de inauguracion
    museo["ano_inauguracion"] = museo["ano_inauguracion"].astype("Int64")
    biblioteca["ano_inauguracion"] = biblioteca["ano_inauguracion"].astype("Int64")

    cine["espacio_incaa"] = cine["espacio_incaa"].str.lower()

    # Creacion de columna numero de telefono: codigo de area + telefono
    museo["numero_de_telefono"] = museo["cod_area"].astype(str) + museo[
        "telefono"
    ].astype(str)
    biblioteca["numero_de_telefono"] = biblioteca["cod_area"].astype(str) + biblioteca[
        "telefono"
    ].astype(str)
    cine["numero_de_telefono"] = cine["cod_area"].astype(str) + cine["telefono"].astype(
        str
    )

    # PROCESAMIENTO PARA CREACION DE TABLA 1 : principal_cultura

    logger.info("Creacion tabla 1 : principal_cultura")

    COLUMNAS_TABLA_1 = [
        "cod_localidad",
        "id_provincia",
        "id_departamento",
        "categoria",
        "provincia",
        "localidad",
        "nombre",
        "domicilio",
        "codigo_postal",
        "numero_de_telefono",
        "mail",
        "web",
    ]

    museo_1 = museo[COLUMNAS_TABLA_1]
    biblioteca_1 = biblioteca[COLUMNAS_TABLA_1]
    cine_1 = cine[COLUMNAS_TABLA_1]

    # Creacion tabla 1 : principal_cultura

    tabla_1 = pd.concat([museo_1, biblioteca_1, cine_1])

    logger.info("Tabla 1 : principal_cultura, creada")
    logger.info(tabla_1.head())
    # PROCESAMIENTO PARA CREACION DE TABLA 2 : totales_cultura

    logger.info("Creacion tabla 2 : totales_cultura")

    # Procesamiento para crear subtabla 'fuente'

    COLUMNAS_TABLA_FUENTE = [
        "cod_localidad",
        "id_provincia",
        "id_departamento",
        "categoria",
        "provincia",
        "localidad",
        "nombre",
        "domicilio",
        "codigo_postal",
        "numero_de_telefono",
        "mail",
        "web",
        "fuente",
    ]

    museo_fuente = museo[COLUMNAS_TABLA_FUENTE]
    biblioteca_fuente = biblioteca[COLUMNAS_TABLA_FUENTE]
    cine_fuente = cine[COLUMNAS_TABLA_FUENTE]

    tabla_fuente = pd.concat([museo_fuente, biblioteca_fuente, cine_fuente])
    tabla_fuente = tabla_fuente.groupby("fuente").size().reset_index()
    tabla_fuente["categoria"] = "fuente"
    tabla_fuente = tabla_fuente.rename(columns={0: "cantidad_de_registros"})
    tabla_fuente = tabla_fuente.rename(columns={"fuente": "subcategoria"})
    tabla_fuente = tabla_fuente[["categoria", "subcategoria", "cantidad_de_registros"]]

    # Procesamiento para crear subtabla 'categoria'

    tabla_categoria = tabla_1.groupby("categoria").size().reset_index()
    tabla_categoria["subcategoria"] = "total_pais"
    tabla_categoria = tabla_categoria.rename(columns={0: "cantidad_de_registros"})
    tabla_categoria = tabla_categoria[
        ["categoria", "subcategoria", "cantidad_de_registros"]
    ]

    # Procesamiento para crear subtabla 'categoria por provincia'

    tabla_prov_cat = tabla_1.groupby(["categoria", "provincia"]).size().reset_index()
    tabla_prov_cat = tabla_prov_cat.rename(columns={"provincia": "subcategoria"})
    tabla_prov_cat = tabla_prov_cat.rename(columns={0: "cantidad_de_registros"})
    tabla_prov_cat = tabla_prov_cat[
        ["categoria", "subcategoria", "cantidad_de_registros"]
    ]

    # Creacion tabla 2 : totales_cultura

    tabla_2 = pd.concat([tabla_categoria, tabla_fuente, tabla_prov_cat])

    logger.info("Tabla 2 : totales_cultura, creada")
    logger.info(tabla_2.head())

    # PROCESAMIENTO PARA CREACION DE TERCERA TABLA : cines_detalle

    logger.info("Creacion tabla 3 : cines_detalle")

    pantallas = cine.groupby("provincia")["pantallas"].sum()
    butacas = cine.groupby("provincia")["butacas"].sum()
    cine["es_incaa"] = (cine["espacio_incaa"] == "si").astype(int)
    espacio_incaa = cine.groupby("provincia")["es_incaa"].sum()

    parte_1 = pd.merge(pantallas, butacas, on="provincia", how="left")

    # Creacion tabla 3 : cines_detalle

    tabla_3 = pd.merge(parte_1, espacio_incaa, on="provincia", how="left").reset_index()

    logger.info("Tabla 3 : cines_detalle, creada")
    logger.info(tabla_3.head())

    # INSERTAR DATOS EN BASE DE DATOS

    logger.info("Insertar datos en base de datos")

    engine = create_engine(DATABASE_URL)

    tabla_1_fecha = tabla_1
    tabla_1_fecha["actualizado"] = datetime.now()

    tabla_2_fecha = tabla_2
    tabla_2_fecha["actualizado"] = datetime.now()

    tabla_3_fecha = tabla_3
    tabla_3_fecha["actualizado"] = datetime.now()

    with engine.connect() as con:
        con.execute("delete from principal_cultura")

    tabla_1_fecha.to_sql(
        name="principal_cultura", con=engine, if_exists="append", index=False
    )

    logger.info("Datos insertados en principal_cultura")

    with engine.connect() as con:
        con.execute("delete from totales_cultura")

    tabla_2_fecha.to_sql(
        name="totales_cultura", con=engine, if_exists="append", index=False
    )

    logger.info("Datos insertados en totales_cultura")

    with engine.connect() as con:
        con.execute("delete from cines_detalle")

    tabla_3_fecha.to_sql(
        name="cines_detalle", con=engine, if_exists="append", index=False
    )

    logger.info("Datos insertados en cines_detalle")


if __name__ == "__main__":
    # logging.info("procesar_archivos")
    procesar_archivos(
        {
            "museos": "data/museos/2022-07/museos-18-07-2022.csv",
            "bibliotecas": "data/bibliotecas/2022-07/bibliotecas-18-07-2022.csv",
            "cines": "data/cines/2022-07/cines-18-07-2022.csv",
        }
    )
