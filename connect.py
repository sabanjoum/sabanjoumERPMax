from mysql.connector import MySQLConnection, Error
from python_mysql_dbconfig import read_db_config

def insert_products(products):
    query = "INSERT INTO product(productID) " \
            "VALUES(%d)"

    try:
        db_config = read_db_config()
        conn = MySQLConnection(**db_config)

        cursor = conn.cursor()
        cursor.executemany(query, books)

        conn.commit()
    except Error as e:
        print('Error:', e)

    finally:
        cursor.close()
        conn.close()

def main():
    products = []
    insert_products(books)

if __name__ == '__main__':
    main()