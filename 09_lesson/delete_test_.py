import psycopg2
from psycopg2 import sql


# Параметры подключения к базе данных
db_connection_params = {
    "dbname": "postgres",
    "user": "postgres",
    "password": "123",
    "host": "localhost",
    "port": 5432
}

# Название таблицы
table_name = "dining_room"

# Переменные для соединения и курсора
conn = None
cur = None

try:
    # Подключаемся к базе данных PostgreSQL
    conn = psycopg2.connect(**db_connection_params)

    # Открываем курсор для выполнения операций с базой данных
    cur = conn.cursor()

    # Выполняем запрос на удаление таблицы
    cur.execute(
        sql.SQL("DROP TABLE IF EXISTS {}").format(sql.Identifier(table_name))
    )

    # Фиксируем изменения
    conn.commit()

    print(f"Таблица '{table_name}' успешно удалена.")

    # Добавляем проверку: пытаемся выбрать данные из таблицы
    try:
        cur.execute(
            sql.SQL("SELECT * FROM {} LIMIT 1").format(sql.Identifier(table_name))
        )
    except psycopg2.errors.UndefinedTable:
        # Если таблица не существует, это ожидаемое поведение
        print(f"Таблица '{table_name}' успешно удалена (проверено через исключение).")
    else:
        # Если таблица все еще существует, вызываем ошибку
        raise AssertionError(f"Таблица '{table_name}' не была удалена.")

except psycopg2.Error as e:
    print(f"Произошла ошибка базы данных: {e}")
except Exception as e:
    print(f"Произошла непредвиденная ошибка: {e}")

finally:
    # Закрываем курсор и соединение, если они были открыты
    if cur is not None:
        cur.close()
    if conn is not None:
        conn.close()