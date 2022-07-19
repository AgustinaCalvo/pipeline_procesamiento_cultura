from sqlalchemy import create_engine, text

engine = create_engine("postgresql://user:pass@localhost:5432/culturagov")

with engine.connect() as con:
    with open("./scripts_sql/crear_tablas.sql") as file:
        query = text(file.read())
        con.execute(query)


# TODO: Agregar logging