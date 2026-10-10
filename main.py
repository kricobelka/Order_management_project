import psycopg
import os

from repositories import customer_repository
from repositories import product_repository
from repositories import order_repository
from models.user import User
from models.admin import Admin
from order_item import OrderItem
from order import Order
from product import Product

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
                
                customer_repository_object = customer_repository.CustomerRepository(cursor)
                product_repository_object = product_repository.ProductRepository(cursor)
                order_repository_object = order_repository.OrderRepository(cursor)
            
                custom_user = None
                
                while True:
                    if custom_user is None:
                        print("1. Login")
                        
                    elif custom_user.role() == "admin":
                        print("""Menu
                            2. Get products
                            3. Get customers
                            4. Get all orders per product
                            7. Exit
                        """)
                    else:
                            
                        print("""Menu
                                    2. Get products
                                    5. Create order and add order item(s)
                                    6. Get my orders
                                    7. Exit
                            """)
                        
                    message = input("Choose option: ")
                        
                    if message == "1" and custom_user is None:
                            email = input("Please enter login: ")
                            
                            customer = customer_repository_object.get_customer(email)
                            if customer is None:
                                print("User not found")
                                continue
                            
                            if customer[3] == "admin":
                                
                                custom_user = Admin(customer[0], customer[1], customer[2])
                                
                            else:
                                custom_user = User(customer[0], customer[1], customer[2])
                                
                            
                    elif message == "2":
                            if custom_user is None:
                                print("Please login first")
                                continue
                            
                            products = product_repository_object.get_products()
                            for product in products:
                                # f"{product.product_id} | "
                                f"{product.product_name} | "
                                f"{product.price} | "
                                f"{product.stock}"
                                # если айди не нужно показывать клиенту, мы его можем не печатть(убратб из принта)
                            
                    elif message == "3":
                            if custom_user is not None and custom_user.role() == "admin":
                                customers = customer_repository_object.get_customers()
                                for customer_id, customer_name, email in customers:
                                    print(f"{customer_id} | {customer_name} | {email}")
                            else:
                                print("Access denied.")
                        

                    elif message == "4":
                            if custom_user is not None and custom_user.role() == "admin":
                                all_product_orders = product_repository_object.get_all_product_orders()
                                for id, pr_name, total_orders, total_revenue in all_product_orders:
                                    print(f"{pr_name} | {total_orders} | {total_revenue}")        
                            else:
                                print("Access denied.")
                            
                    elif message == "5":
                            if custom_user is not None and custom_user.role() == "user":
                                try:
                                    order = order_repository_object.create_order(custom_user.user_id)
                                except ValueError as e:
                                    print(e)
                                else:
                                    print(f"Order {order.order_id} has been created")
                                
                                    while True:

                                        products = product_repository_object.get_products()
                                        for product in products:
                                            f"{product.product_id} | "
                                            f"{product.product_name} | "
                                            f"{product.price} | "
                                            f"{product.stock}"

                                        try:
                                            product_id = int(input("Product id that must be added: "))
                                            quantity = int(input("Quantity of product: "))
                                        except ValueError:
                                            print("Product_id/quantity must be a number")
                                            continue

                                        product_object = None

                                        for product in products:
                                            if product.product_id == product_id:
                                                product_object = product
                                                break

                                        if product_object is None:
                                             print("Product not found")
                                             continue
                                        
                                        try:
                                            product = product_repository_object.get_product_by_id(product_object)
                                            order_repository_object.add_order_item(order, product, quantity)
                                            print(f"Product: {product.product_name}, q-ty:  {quantity} added to order {order.order_id}")

                                        except ValueError as e:
                                            print(e)
                                            continue

                                        else:
                                            answer = input("Do you want to add another product? yes/no").strip().lower()
                                            if answer == "no":
                                                break
                            else:
                                print ("Access denied")
                            
                    elif message == "6":
                            if custom_user is not None and custom_user.role() == "user":

                                while True:
                                    orders = customer_repository_object.get_my_orders(custom_user.user_id)

                                    for order in orders:
                                        print(f"Order id: {order.id}, total_sum: {order.total_sum}")
                                    
                                    try:
                                        order_id = int(input("Id of the required order; if you need to quit, press '0': "))
                                        if order_id == 0:
                                             break

                                    except ValueError:
                                        print("Order id must be a number")
                                        continue

                                    selected_order = None

                                    for order in orders:
                                        if order.id == order_id:
                                            selected_order = order
                                            break

                                    if selected_order is None:
                                        print("Order not found. Error")
                                        continue

                                    order_info = order_repository_object.get_full_order_information(selected_order)
                                    
                                    for order_id, product_name, product_price, quantity, item_total_price in order_info:
                                                print(f"Product name: {product_name}\n"
                                                f"Price: {product_price}\n"
                                                f"Quantity: {quantity}\n"
                                                f"Total price: {item_total_price}")
                                    
                            else:
                                print ("Access Error")
                            
                    elif message == "7":
                            break

                        #     order_items = get_order_items(cursor, order_id)
                        #     for item in order_items:
                        #         print(f"order_id: {item[0]}, product_name: {item[1]}, price: {item[2]}, quantity: {item[3]}, item_total: {item[4]}")
