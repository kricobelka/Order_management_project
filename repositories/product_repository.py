from product import Product

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
        products_result = []

        for product in products:
            products_result.append(Product.from_db_tuple(product))
             
        return products_result

    def get_product_by_id(self, product):

        self.cursor.execute("""SELECT id, name, price, stock 
                                FROM products 
                                WHERE id = %s;
                                """, (product.product_id, ))
        
        product_result = self.cursor.fetchone()

        if product_result is None:
            raise ValueError("Product is not found")

        return Product.from_db_tuple(product_result)     
    
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
 


         