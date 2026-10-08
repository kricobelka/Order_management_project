
class UserApplication:

    def __init__(self, cursor, user):
        self.cursor = cursor
        self.user = user

    def get_role(self):
        return self.user.role()

    def get_method_list(self):
        return ["get_products", "create_order", "add_order_item", "get_order_total", "get_order_items"]
