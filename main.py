import psycopg
import os

print(psycopg.__version__)

def get_customers(cursor):

    cursor.execute("""
                SELECT id, name, email
                FROM customers
                ORDER BY id;
            """)
    
    customers = cursor.fetchall()

    return customers

def get_products(cursor):

    cursor.execute("""
                SELECT id, name, price, stock
                FROM products
                ORDER BY id
    """)

    products = cursor.fetchall()

    return products

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

def create_order(cursor, customer_id):

    cursor.execute("""SELECT id FROM customers
        WHERE id = %s;
        """, (customer_id, ))
    
    result = cursor.fetchone()
    
    if result is None:
            raise ValueError("Customer is not found")

    cursor.execute("""INSERT INTO orders_new (customer_id)
                    VALUES (%s) RETURNING id;
                    """, (customer_id, ))

    order_id = cursor.fetchone()[0]
    return order_id

def add_order_item(cursor, order_id, product_id, quantity):

    cursor.execute("""SELECT id, stock FROM products 
                    WHERE id = %s;
                    """, (product_id, ))

    result = cursor.fetchone()

    if result is None:
            raise ValueError("Product is not foound")
    
    _, stock = result

    if quantity <= 0:
        raise ValueError("Please insert a valid quantity")
    
    if quantity > stock:    
        raise ValueError("Not enough product at stock")
    
    cursor.execute("""
                        INSERT INTO order_items (order_id, product_id, quantity)
                        VALUES (%s, %s, %s);
                        """, (order_id, product_id, quantity))
    
    cursor.execute("""UPDATE products 
                    SET stock = stock - %s
                    WHERE id = %s;
                    """, (quantity, product_id))


def get_order_total(cursor, order_id):

    cursor.execute("""SELECT orders_new.id, COALESCE((SUM(products.price * order_items.quantity)), 0)
                    FROM orders_new
                    LEFT JOIN order_items ON order_items.order_id = orders_new.id
                    LEFT JOIN products ON order_items.product_id = products.id
                        WHERE orders_new.id = %s
                        GROUP BY orders_new.id;
                    """, (order_id, ))
    
    order = cursor.fetchone()
    return order

def get_order_items(cursor, order_id):
    cursor.execute("""SELECT orders_new.id, products.name, products.price, order_items.quantity,
                                                                products.price * order_items.quantity AS item_total
                        FROM order_items
                            JOIN products ON order_items.product_id = products.id
                            JOIN orders_new ON order_items.order_id = orders_new.id
                        WHERE order_items.order_id = %s;
     """, (order_id, ))

    order_items = cursor.fetchall()

    return order_items
     

    # более длинный способ:
    # cursor.execute("""SELECT id
    #                 FROM products
    #                 WHERE products.id = %s;""",
    #                 (product_id, ))

    # result = cursor.fetchone()[0]

    # if result is None:
    #     print("Product not found")

    # else:
    #     cursor.execute("""
    #                 SELECT stock FROM products
    #                 WHERE products.id = %s;""",
    #                 (product_id, ))
    
    #     stock = cursor.fetchone()

    #     if quantity > stock:
    #         print("Not enough quantity at stock")

        # else:
            # cursor.execute("""
            #             INSERT INTO order_items (order_id, product_id, quantity)
            #             VALUES (%s, %s, %s);
            #             """, (order_id, product_id, quantity))

if __name__ == "__main__":

    with psycopg.connect(

        dbname = os.getenv("DB_NAME"),
        host = os.getenv("DB_HOST"),
        port = os.getenv("DB_PORT"),
        user = os.getenv("DB_USER"),
        password = os.getenv("DB_PASSWORD")

    ) as connection:
        print("Connected!")

        with connection.cursor() as cursor:
                
                customers = get_customers(cursor)

                for customer_id, customer_name, email in customers:
                    print(f"{customer_id} | {customer_name} | {email}")

                products = get_products(cursor)

                for id, name, price, stock in products:
                        print(f"{id} | {name} | {price} | {stock}")
                # если айди не нужно показывать клиенту, мы его можем не печатть(убратб из принта)

                customer_id = int(input("Please insert customer id whose orders must be received: "))
                customer_orders = get_customer_orders(cursor, customer_id)

                print(customer_orders)
                

                customer_id = int(input("Please provide customer id to which order shall be added: "))

                try:
                    order_id = create_order(cursor, customer_id)
                except ValueError as e:
                    print(e)

                else:
                    print(f"Order {order_id} has been created")

                    while True:

                        try: 
                            product_id = int(input("Product id to be added: "))
                        except ValueError:
                            print("Product id must be a number")
                            continue
                    
                        try:
                            quantity = int(input("Q-ty of products to be added: "))
                        except ValueError:
                            print("Quantity id must be a number")
                            continue
                                    
                        try:
                            add_order_item(cursor, order_id, product_id, quantity)
                            print(f"Product: {product_id}, q-ty:  {quantity} added to order {order_id}")
                        except ValueError as e:
                            print(e)
                    
                        answer = input("Do you want to add another product? yes/no")
                        if answer != "yes":
                            break
                    
                    order_total = get_order_total(cursor, order_id)
                    if order_total is None:
                        print(f"Order not found")
                    else:
                        order_id, total = order_total
                        print(order_id)
                        print(total)

                    order_items = get_order_items(cursor, order_id)
                    for item in order_items:
                            print(f"order_id: {item[0]}, product_name: {item[1]}, price: {item[2]}, quantity: {item[3]}, item_total: {item[4]}")


    