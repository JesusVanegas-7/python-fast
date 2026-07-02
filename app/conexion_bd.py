from sqlmodel import SQLModel, create_engine

sqlite_nombre = "database.db"

sqlite_url = f"sqlite:///{sqlite_nombre}"

engine = create_engine(sqlite_url, echo=True)


def crear_db_y_tablas():
    SQLModel.metadata.create_all(engine)