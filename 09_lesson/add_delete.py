from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String
from sqlalchemy import inspect


DB_CONNECTION_STRING = "postgresql://postgres:123@localhost:5432/postgres"

engine = create_engine(DB_CONNECTION_STRING)

def create_dining_room_table():
    metadata = MetaData()

    dining_room_table = Table(
        'dining_room', metadata,
        Column('id', Integer, primary_key=True),
        Column('name', String, nullable=False),
        Column('capacity', Integer),
        Column('location', String)
    )

    inspector = inspect(engine)

    if 'dining_room' not in inspector.get_table_names(schema='public'):
        try:
            metadata.create_all(engine)
            print("Таблица 'dining_room' успешно создана!")
        except Exception as e:
            print("Ошибка при создании таблицы:", e)
    else:
        print("Таблица 'dining_room' уже существует.")


def test_db_connection():
    inspector = inspect(engine)


    table_names = inspector.get_table_names(schema='public')

    if table_names:
        print("Таблицы в базе данных:")
        for table in table_names:
            print(f"- {table}")
    else:
        print("В базе данных нет таблиц.")



def drop_dining_room_table():
    metadata = MetaData()

    dining_room_table = Table(
        'dining_room', metadata,
        Column('id', Integer, primary_key=True),
        Column('name', String, nullable=False),
        Column('capacity', Integer),
        Column('location', String)
    )

    inspector = inspect(engine)
    if 'dining_room' in inspector.get_table_names(schema='public'):
        try:
            dining_room_table.drop(engine)
            print("Таблица 'dining_room' успешно удалена!")
        except Exception as e:
            print("Ошибка при удалении таблицы:", e)
    else:
        print("Таблица 'dining_room' не существует.")