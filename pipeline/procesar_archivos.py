import pandas as pd
import numpy as np

museo = pd.read_csv("./data/museos/2022-07/museos-15-07-2022.csv")
biblioteca = pd.read_csv("./data/bibliotecas/2022-07/bibliotecas-15-07-2022.csv")
cine = pd.read_csv("./data/cines/2022-07/cines-15-07-2022.csv")

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
    "espacio_INCAA",
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

cine["espacio_INCAA"] = cine["espacio_INCAA"].str.lower()

# Creacion de columna numero de telefono: codigo de area + telefono
museo["numero_de_telefono"] = museo["cod_area"].astype(str) + museo["telefono"].astype(
    str
)
biblioteca["numero_de_telefono"] = biblioteca["cod_area"].astype(str) + biblioteca[
    "telefono"
].astype(str)
cine["numero_de_telefono"] = cine["cod_area"].astype(str) + cine["telefono"].astype(str)

# PROCESAMIENTO PARA CREACION DE TABLA 1 : #TODO:ELEGIR NOMBRE DE TABLA

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

# PRIMER TABLA
tabla_1 = pd.concat([museo_1, biblioteca_1, cine_1])

# PROCESAMIENTO PARA CREACION DE SEGUNDA TABLA

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
tabla_prov_cat = tabla_prov_cat[["categoria", "subcategoria", "cantidad_de_registros"]]

# Creacion tabla 2 : #TODO : tabla_cat_fuente_registros

tabla_2 = pd.concat([tabla_categoria, tabla_fuente, tabla_prov_cat])

print(tabla_2.head())
# print(biblioteca_1.head())
# print(cine_1.head())
