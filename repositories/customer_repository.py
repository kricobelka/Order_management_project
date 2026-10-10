from customer_orders import CustomerOrders
class CustomerRepository:
    def __init__(self, cursor):
        self.cursor = cursor

        
    def get_customers(self):

        self.cursor.execute("""
                                        SELECT id, name, email, role
                                        FROM customers
                                        ORDER BY id;
                    """)
                            
        customers = self.cursor.fetchall()

        return customers
    
    def get_customer(self, customer_email):
        
        self.cursor.execute("""SELECT id, name, email, role FROM customers
                            WHERE customers.email = %s;
                            """, (customer_email, ))
        
        customer = self.cursor.fetchone()
        return customer
    
    def get_my_orders(self, customer_id):
        
        self.cursor.execute("""SELECT orders_new.id, 
                                SUM(products.price * order_items.quantity) AS total_sum
                            FROM orders_new
                                JOIN customers ON orders_new.customer_id = customers.id
                                JOIN order_items ON orders_new.id = order_items.order_id
                                JOIN products ON products.id = order_items.product_id
                            WHERE customers.id = %s
                            GROUP BY orders_new.id;
                            """, (customer_id, ))
        
        orders = self.cursor.fetchall()
        order_list = []
        for order in orders:
            order_list.append(CustomerOrders.from_db_tuple(order))

        return order_list


    
