class CustomerOrders:

    def __init__(self, id, total_sum):
        self.id = id
        self.total_sum = total_sum

    @classmethod
    def from_db_tuple(cls, row):
        return cls(row[0], row[1])