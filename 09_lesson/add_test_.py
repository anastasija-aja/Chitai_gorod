from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String
from sqlalchemy import inspect


db_params = {
    'dbname': 'postgres',
    'user': 'postgres',
    'password': '123',
    'host': 'localhost'
}


engine = create_engine(
    f"postgresql+psycopg2://{db_params['user']}:{db_params['password']}@"
    f"{db_params['host']}/{db_params['dbname']}"
)


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

    if not inspector.has_table('classroom'):
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

    assert inspector.has_table('classroom'), "Тест не пройден: таблица 'classroom' отсутствует!"
    print("Тест успешно пройден: таблица 'classroom' существует!")