
import psycopg

def get_products(cursor):

    cursor.execute("""
                SELECT id, name, price, stock
                FROM products
                ORDER BY id
    """)

    products = cursor.fetchall()

    return products