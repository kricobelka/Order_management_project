from product import Product
from notFoundError import NotFoundError

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

    def add_new_product(self, product):

        self.cursor.execute("""
                        INSERT INTO products (name, price, stock)
                        VALUES (%s, %s, %s)
                        RETURNING id, name, price, stock;
        """, (product.product_name, product.price, product.stock))

        new_product = self.cursor.fetchone()
        return Product.from_db_tuple(new_product)


    def update_product_information(self, product_id, info_to_change, new_value):

        allowed_fields = {
        "name": "name",
        "price": "price",
        "stock": "stock"
        }

        if info_to_change not in allowed_fields:
            raise KeyError("Invalid product field")
        
        column = allowed_fields[info_to_change]

        if info_to_change == "price" and new_value < 0:
            raise ValueError("Price cannot be negative")
        
        if info_to_change == "stock" and new_value < 0:
            raise ValueError("Stock cannot be negative")

        self.cursor.execute(f"""
                            UPDATE products SET {column} = %s
                            WHERE id = %s RETURNING id;
        """, (new_value, product_id))
        

        updated_product_id = self.cursor.fetchone()

        if updated_product_id is None:
            raise NotFoundError(f"Product with {product_id} is not found")


    def search_product_by_name(self, product_name):

        if not isinstance(product_name, str):
            raise ValueError("Product name must be a string")
                
        self.cursor.execute("""SELECT id, name, price, stock
                            FROM products
                            WHERE name = %s;
        """, (product_name, ))
        
        found_product = self.cursor.fetchone()

        if found_product is None:
            raise NotFoundError(f"Product with name {product_name} hasn't been found")

        return Product.from_db_tuple(found_product)


    def filter_by_price_and_stock(self, min_price, max_price):

        self.cursor.execute("""SELECT id, name, price, stock
                            FROM products
                            WHERE stock > 0
                            AND price >= %s AND price <= %s
                            """, (min_price,  max_price))
        
        filtered_products = [Product.from_db_tuple(product) for product in self.cursor.fetchall()]
        
        return filtered_products

    def update_stock(self, product_id, new_stock):
        
        self.cursor.execute("""UPDATE products SET stock = %s
                            WHERE id = %s
                            RETURNING id;
        """, (new_stock, product_id))

        updated_product_id = self.cursor.fetchone()
        if updated_product_id is None:
            raise NotFoundError("Product not found")

    

        
        