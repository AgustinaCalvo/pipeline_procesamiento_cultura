CREATE TABLE IF NOT EXISTS cines_detalle (
   provincia VARCHAR(50) unique NOT NULL PRIMARY KEY ,
   pantallas INT,
   butacas INT,
   es_incaa INT,
   actualizado TIMESTAMP NOT NULL
);

CREATE TABLE IF NOT EXISTS tabla_cat_fuente_registros (
   categoria VARCHAR(100),
   subcategoria VARCHAR(100),
   cantidad_de_registros INT,
   actualizado TIMESTAMP NOT null,
   primary KEY(categoria, subcategoria)
);
	

CREATE TABLE IF NOT EXISTS tabla_unica (
    cod_localidad INT,
	id_provincia INT,
	id_departamento INT,
	categoria VARCHAR(100),
	provincia VARCHAR(100),
	localidad VARCHAR(100),
	nombre VARCHAR(100),
	domicilio VARCHAR(100),
	codigo_postal INT,
	numero_de_telefono INT,
	mail VARCHAR(100),
	web VARCHAR(100),
    actualizado TIMESTAMP NOT NULL
);