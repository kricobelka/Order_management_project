import psycopg

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