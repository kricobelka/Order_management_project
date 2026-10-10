class OrderItem:
    def __init__(self, product, quantity):
        self.product = product
        self.quantity = quantity

    @property
    def quantity(self):
        return self._quantity

    @quantity.setter
    def quantity(self, value):
        if value <= 0:
            raise ValueError("Quantity must be positive")

        self._quantity = value
        