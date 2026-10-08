class OrderRepository:
    def __init__(self, cursor):
        self.cursor = cursor
        
    def create_order(self, customer_id):
        self.cursor.execute("""SELECT id FROM customers
            WHERE id = %s;
            """, (customer_id, ))
        
        result = self.cursor.fetchone()
        
        if result is None:
                raise ValueError("Customer is not found")

        self.cursor.execute("""INSERT INTO orders_new (customer_id)
                        VALUES (%s) RETURNING id;
                        """, (customer_id, ))

        order_id = self.cursor.fetchone()[0]
        return order_id

    def add_order_item(self, order_id, product_id, quantity):

        self.cursor.execute("""SELECT id, stock FROM products 
                        WHERE id = %s;
                        """, (product_id, ))

        result = self.cursor.fetchone()

        if result is None:
                raise ValueError("Product is not found")
        
        _, stock = result

        if quantity <= 0:
            raise ValueError("Please insert a valid quantity")
        
        if quantity > stock:    
            raise ValueError("Not enough product at stock")
        
        self.cursor.execute("""
                            INSERT INTO order_items (order_id, product_id, quantity)
                            VALUES (%s, %s, %s);
                            """, (order_id, product_id, quantity))
        
        self.cursor.execute("""UPDATE products 
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


    def get_full_order_information(self, order_id):
        self.cursor.execute("""SELECT orders_new.id, products.name, products.price, order_items.quantity,
                                products.price * order_items.quantity AS item_total
                            FROM order_items
                                JOIN products ON order_items.product_id = products.id
                                JOIN orders_new ON order_items.order_id = orders_new.id
                            WHERE order_items.order_id = %s;
                            """, (order_id, ))

        order_items = self.cursor.fetchall()
        return order_items



    # not necessary in this application:
    # def get_order_total(self, order_id):
    
    #         self.cursor.execute("""SELECT orders_new.id, COALESCE((SUM(products.price * order_items.quantity)), 0)
    #                         FROM orders_new
    #                         LEFT JOIN order_items ON order_items.order_id = orders_new.id
    #                         LEFT JOIN products ON order_items.product_id = products.id
    #                             WHERE orders_new.id = %s
    #                             GROUP BY orders_new.id;
    #                         """, (order_id, ))
            
    #         order = self.cursor.fetchone()
    #         return order