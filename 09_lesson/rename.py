from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, inspect, text

db_connection_string = "postgresql://postgres:123@localhost:5432/postgres"
engine = create_engine(db_connection_string)

def create_classroom_room_table():
    metadata = MetaData()

    classroom_room_table = Table(
        'classroom_room', metadata,
        Column('id', Integer, primary_key=True),
        Column('name', String, nullable=False),
        Column('capacity', Integer),
        Column('location', String)
    )

    try:
        metadata.create_all(engine)
        print("Таблица 'classroom_room' успешно создана!")
    except Exception as e:
        print("Ошибка при создании таблицы:", e)

def rename_classroom_room_table(new_name):
    if not new_name.isidentifier():
        print("Недопустимое имя таблицы")
        return

    try:
        with engine.connect() as connection:
            trans = connection.begin()  # Начало транзакции
            query = text("ALTER TABLE classroom_room RENAME TO :new_name")
            connection.execute(query, {"new_name": new_name})
            trans.commit()  # Подтверждение транзакции
            print(f"Таблица 'classroom_room' успешно переименована в '{new_name}'!")
    except Exception as e:
        print("Ошибка при переименовании таблицы:", e)

def test_db_connection():
    inspector = inspect(engine)
    table_names = inspector.get_table_names()

    if table_names:
        print("Таблицы в базе данных:")
        for table in table_names:
            print(f"- {table}")
    else:
        print("В базе данных нет таблиц.")