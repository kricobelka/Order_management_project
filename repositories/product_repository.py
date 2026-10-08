

class ProductRepository:
    
    def __init__(self, cursor):
        self.cursor = cursor
        
    def get_products(self):

        self.cursor.execute("""
                    SELECT id, name, price, stock
                    FROM products
                    ORDER BY id
        """)

        products = self.cursor.fetchall()

        return products
    
    def get_all_product_orders(self):
    
            self.cursor.execute("""
                                SELECT products.id, products.name, 
                                COUNT(DISTINCT order_items.order_id) AS total_orders,
                                    SUM(order_items.quantity * products.price) AS total_revenue
                            FROM products
                            JOIN order_items ON products.id = order_items.product_id
                            GROUP BY products.id, products.name;""")
    
            all_product_orders = self.cursor.fetchall()
                                
            return all_product_orders