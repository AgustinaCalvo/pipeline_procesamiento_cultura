from sqlalchemy import create_engine, text
from pipeline.config import DATABASE_URL
from pipeline.config import logger

engine = create_engine(DATABASE_URL)

logger.info("Creando tablas SQL")
with engine.connect() as con:
    with open("./scripts_sql/crear_tablas.sql") as file:
        query = text(file.read())
        con.execute(query)


logger.info("Tablas SQL creadas")
