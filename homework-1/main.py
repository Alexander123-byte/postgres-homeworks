"""
Скрипт для заполнения данными таблиц в БД Postgres.
"""

import csv
import psycopg2
from psycopg2 import sql

db_params = {
    'host': 'localhost',
    'database': 'north',
    'user': 'postgres',
    'password': 'rewty76',
}

customers_csv = 'north_data/customers_data.csv'
employees_csv = 'north_data/employees_data.csv'
orders_csv = 'north_data/orders_data.csv'


def create_connection():
    """
    Создает и возвращает соединение с базой данных PostgreSQL.

    Returns:
        psycopg2.extensions.connection: Объект соединения с базой данных.
    """
    return psycopg2.connect(**db_params)


def copy_data_from_csv(file_path, table_name, connection):
    """
    Копирует данные из CSV-файла в указанную таблицу базы данных PostgreSQL.

    Args:
        file_path (str): Путь в CSV-файлу.
        table_name (str): Имя целевой таблицы в базе данных.
        connection (psycopg2.extensions.connection): Объект соединения с базой данных.

    Raises:
        psycopg2.Error: В случае ошибок при взаимодействии с базой данных.
    """
    with connection.cursor() as cursor:
        with open(file_path, 'r', encoding='utf-8') as file:
            # Пропустить заголовок
            next(file)

            # Читать строки CSV
            for row in csv.reader(file):
                # Подготовить строку для вставки в SQL
                values_template = ', '.join(["%s"] * len(row))
                insert_query = sql.SQL(f'INSERT INTO {table_name} VALUES ({values_template})')

                # Вставить строку в таблицу
                cursor.execute(insert_query, row)

    connection.commit()

    print(f"Данные успешно добавлены в таблицу {table_name}")


def main():
    """
    Основная функция для выполнения загрузки данных из CSV-файлов в базу данных.
    """
    connection = create_connection()

    # Загрузка данных из CSV-файлов
    copy_data_from_csv(customers_csv, 'customers', connection)
    copy_data_from_csv(employees_csv, 'employees', connection)
    copy_data_from_csv(orders_csv, 'orders', connection)

    connection.close()


if __name__ == '__main__':
    main()
