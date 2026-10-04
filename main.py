import psycopg
import os

print(psycopg.__version__)


from repositories.customer_repository import get_customers, get_customer_orders
from repositories.product_repository import get_products
from repositories.order_repository import create_order, add_order_item, get_order_total, get_order_items
     
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


    