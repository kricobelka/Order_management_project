 # SQL exersizes with database
        # cursor.execute("""
        #                 SELECT customers.name AS customer_name,
        #                     orders_new.id AS order_id,
        #                         products.name AS product_name,
        #                         products.price AS price,
        #                         order_items.quantity AS quantity,
        #                         (products.price * order_items.quantity) AS item_total
        #                 FROM customers
        #                     JOIN orders_new ON customers.id = orders_new.customer_id
        #                     JOIN order_items ON orders_new.id = order_items.order_id
        #                     JOIN products ON products.id = order_items.product_id;
        #                 """)

        # rows = cursor.fetchall()

        # for row in rows:
        #     print(row)

        # cursor.execute("""
        #                 SELECT orders_new.id AS order_id, customers.name AS customer_name, 
        #                 SUM(products.price * order_items.quantity) AS order_total
        #                 FROM orders_new
        #                 JOIN customers ON orders_new.customer_id = customers.id
        #                 JOIN order_items ON order_items.order_id = orders_new.id
        #                 JOIN products ON order_items.product_id = products.id
        #                 GROUP BY orders_new.id, customers.name
        #                 ORDER BY order_id;
        #                 """)

        # rows = cursor.fetchall()

        # print("Статистика по каждому заказу")
        # for row in rows:
        #     print(row)


        # cursor.execute("""
        #                 SELECT customers.name, COUNT(DISTINCT orders_new.id) AS order_count,
        #                 COALESCE(SUM(products.price * order_items.quantity), 0) AS total_spent
        #                 FROM customers
        #                 LEFT JOIN orders_new ON customers.id = orders_new.customer_id
        #                 LEFT JOIN order_items ON orders_new.id = order_items.order_id
        #                 LEFT JOIN products ON products.id = order_items.product_id
        #                 GROUP BY customers.name;
        # """)
        
        # rows = cursor.fetchall()
        
        # print("Статистика по каждому клиенту")
        # for row in rows:
        #     print(row)


        # cursor.execute("""
        #                 SELECT customers.name, SUM(products.price * order_items.quantity) AS total_spent
        #                 FROM customers
        #                 JOIN orders_new
        #                     ON customers.id = orders_new.customer_id
        #                 JOIN order_items
        #                     ON orders_new.id = order_items.order_id
        #                 JOIN products
        #                     ON products.id = order_items.product_id
        #                 GROUP BY customers.name, customers.id
        #                 HAVING SUM(products.price * order_items.quantity) > 1000;
        # """)

        # rows = cursor.fetchall()
                
        # print("Клиенты которые потратили более 1000")
        # for row in rows:
        #     print(row)


        # cursor.execute("""
        #                 SELECT products.name AS product_name, COUNT(order_items.quantity) AS sold_quantity
        #                 FROM products
        #                 JOIN order_items
        #                     ON products.id = order_items.product_id
        #                 GROUP BY products.name, products.id;
        # """)

        # rows = cursor.fetchall()
                        
        # print("Для каждого товара показать, сколько единиц было продано.")
        # for row in rows:
        #     print(row)



        # cursor.execute("""
        #                 SELECT products.name AS product_name
        #                 FROM products
        #                 LEFT JOIN order_items
        #                     ON products.id = order_items.product_id
        #                 GROUP BY products.id, products.name
        #                 HAVING COUNT(order_items.product_id) = 0;
        #         """)

        # rows = cursor.fetchall()
                                        
        # print("Показать товары, на которые не было заказов.")
        # for row in rows:
        #     print(row)


        # print("Second option")

        # cursor.execute("""
        #                 SELECT products.name
        #                 FROM products
        #                 LEFT JOIN order_items
        #                     ON products.id = order_items.product_id
        #                 WHERE order_items.product_id IS NULL;
        # """)


        # rows = cursor.fetchall()
                                
        # print("Показать товары, на которые не было заказов.")
        # for row in rows:
        #     print(row)
        

        # cursor.execute("""
        #                 SELECT orders_new.id AS order_id, 
        #                 customers.name AS customer_name,
        #                     SUM(products.price * order_items.quantity) AS order_total
        #             FROM orders_new
        #                 JOIN customers ON customers.id = orders_new.customer_id
        #                 JOIN order_items ON order_items.order_id = orders_new.id
        #                 JOIN products ON order_items.product_id = products.id
        #             GROUP BY orders_new.id, customers.name
        #             HAVING SUM(products.price * order_items.quantity) > (

        #                 SELECT AVG(order_total)
        #                 FROM (
        #                     SELECT orders_new.id, SUM(products.price * order_items.quantity) AS order_total
        #                     FROM products
        #                         JOIN order_items ON order_items.product_id = products.id
        #                         JOIN orders_new ON order_items.order_id = orders_new.id
        #                     GROUP BY orders_new.id
        #                     ) AS order_totals

        #                 );
        #                         """)

        # rows = cursor.fetchall()
                                        
        # print("Заказы, сумма которых выше средней стоимости всех заказов.")
        # for row in rows:
        #     print(row)

        # cursor.execute("""
        #             WITH orders_total AS (
        #             SELECT orders_new.id AS order_id, customers.id AS customer_id,
        #                 SUM(products.price * order_items.quantity) AS order_total
        #             FROM orders_new
        #                 JOIN customers ON customers.id = orders_new.customer_id
        #                 JOIN order_items ON order_items.order_id = orders_new.id
        #                 JOIN products ON order_items.product_id = products.id
        #                 GROUP BY orders_new.id, customers.id
        #             )

        #             SELECT customers.name,
        #                 COUNT(orders_total.order_id), SUM(orders_total.order_total)
        #             FROM orders_total
        #             JOIN customers ON orders_total.customer_id = customers.id
        #             GROUP BY customers.name, customers.id;
        # """)