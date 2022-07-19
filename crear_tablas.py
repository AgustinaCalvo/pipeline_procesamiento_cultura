from sqlalchemy import create_engine, text
from pipeline.config import DATABASE_URL

engine = create_engine(DATABASE_URL)

with engine.connect() as con:
    with open("./scripts_sql/crear_tablas.sql") as file:
        query = text(file.read())
        con.execute(query)


# TODO: Agregar logging
