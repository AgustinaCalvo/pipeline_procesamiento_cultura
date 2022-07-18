CREATE TABLE IF NOT EXISTS principal_cultura (
    cod_localidad VARCHAR,
	id_provincia VARCHAR,
	id_departamento VARCHAR,
	categoria VARCHAR,
	provincia VARCHAR,
	localidad VARCHAR,
	nombre VARCHAR,
	domicilio VARCHAR,
	codigo_postal VARCHAR,
	numero_de_telefono VARCHAR,
	mail VARCHAR,
	web VARCHAR,
    actualizado TIMESTAMP NOT NULL
);

CREATE TABLE IF NOT EXISTS totales_cultura (
   categoria VARCHAR,
   subcategoria VARCHAR,
   cantidad_de_registros INT,
   actualizado TIMESTAMP NOT null,
   primary KEY(categoria, subcategoria)
);

CREATE TABLE IF NOT EXISTS cines_detalle (
   provincia VARCHAR unique NOT NULL PRIMARY KEY ,
   pantallas INT,
   butacas INT,
   es_incaa INT,
   actualizado TIMESTAMP NOT NULL
);