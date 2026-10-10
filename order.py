class Order:

    def __init__(self, order_id, customer_id):
        self.order_id = order_id
        self.customer_id = customer_id
        self.order_items = []


    def add_order_item(self, order_item):
        self.order_items.append(order_item)