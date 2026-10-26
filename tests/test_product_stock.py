
import pytest
from decimal import Decimal

from product import Product

def test_product_stock():
    product = Product(1,  "Watch", 150, 10)
    assert product.stock == 10


def test_product_initialization():
    product = Product(product_id=None, product_name="Server", price=3000, stock=5)
    assert product.stock == 5
    assert product.price == Decimal("3000")


@pytest.mark.parametrize("field_name, invalid_value", [
    ("price", Decimal("-0.01")),
     ("stock", -1)
])

def test_product_price_stock_nonnegative(field_name, invalid_value):
    product = Product(product_id=None, product_name="Server", price=3000, stock=5)

    with pytest.raises(ValueError):
        setattr(product, field_name, invalid_value)
