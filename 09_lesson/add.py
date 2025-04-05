from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String
from sqlalchemy import inspect


db_connection_string = "postgresql://postgres:123@localhost:5432/postgres"

engine = create_engine(db_connection_string)


try:
    with engine.connect() as connection:
        print("Подключение успешно!")
except Exception as e:
    print("Ошибка подключения:", e)


def create_classroom_table():

    metadata = MetaData()

    classroom_table = Table(
        'classroom', metadata,
        Column('id', Integer, primary_key=True),
        Column('name', String, nullable=False),
        Column('capacity', Integer),
        Column('location', String)
    )

    inspector = inspect(engine)
    if 'classroom' not in inspector.get_table_names():
        try:
            metadata.create_all(engine)
            print("Таблица 'classroom' успешно создана!")
        except Exception as e:
            print("Ошибка при создании таблицы:", e)
    else:
        print("Таблица 'classroom' уже существует.")


def test_db_connection():

    inspector = inspect(engine)

    table_names = inspector.get_table_names()
    print("Таблицы в базе данных:", table_names)