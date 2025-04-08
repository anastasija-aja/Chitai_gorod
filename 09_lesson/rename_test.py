import psycopg2
from psycopg2 import sql

# Строка подключения к базе данных
db_connection_params = {
    "dbname": "postgres",
    "user": "postgres",
    "password": "123",
    "host": "localhost",
    "port": 5432
}

def check_connection():
    """Проверяет соединение с базой данных."""
    try:
        with psycopg2.connect(**db_connection_params) as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT 1")
                result = cursor.fetchone()
                if result and result[0] == 1:
                    print("Соединение с базой данных установлено")
    except Exception as e:
        print(f"Ошибка подключения к базе данных: {e}")


def rename_gym_table(large_gym):
    """Переименовывает таблицу gym и выводит список таблиц до и после переименования."""
    try:
        with psycopg2.connect(**db_connection_params) as conn:
            with conn.cursor() as cursor:
                # Получаем список всех таблиц в схеме public до переименования
                cursor.execute("""
                    SELECT table_name
                    FROM information_schema.tables
                    WHERE table_schema = 'public'
                """)
                tables_before = cursor.fetchall()

                print("Таблицы в базе данных до переименования:")
                for table in tables_before:
                    print(f"- {table[0]}")

                # SQL-запрос для переименования таблицы
                query = sql.SQL("ALTER TABLE {} RENAME TO {}").format(
                    sql.Identifier("gym"),
                    sql.Identifier(large_gym)  # Используем переданное имя напрямую
                )
                cursor.execute(query)
                conn.commit()  # Фиксируем транзакцию
                print(f"Таблица 'gym' успешно переименована в '{large_gym}'!")

                # Получаем список всех таблиц в схеме public после переименования
                cursor.execute("""
                    SELECT table_name
                    FROM information_schema.tables
                    WHERE table_schema = 'public'
                """)
                tables_after = cursor.fetchall()

                print("Таблицы в базе данных после переименования:")
                for table in tables_after:
                    print(f"- {table[0]}")

    except Exception as e:
        print(f"Ошибка при переименовании таблицы: {e}")


# Пример использования функций
if __name__ == "__main__":
    check_connection()
    rename_gym_table("large_gym")