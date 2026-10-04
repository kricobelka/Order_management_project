import psycopg

def get_customers(cursor):

    cursor.execute("""
                SELECT id, name, email
                FROM customers
                ORDER BY id;
            """)
    
    customers = cursor.fetchall()

    return customers


def get_customer_orders(cursor, customer_id):

    cursor.execute("""
                    SELECT orders_new.id, customers.name
                    FROM orders_new
                    JOIN customers ON customers.id = orders_new.customer_id
                    WHERE customers.id = %s;
                    """,
                    (customer_id,))

    customer_orders = cursor.fetchall()
     
    return customer_orders
