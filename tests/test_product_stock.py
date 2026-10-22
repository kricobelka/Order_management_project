
import pytest

from product import Product

def test_product_stock():
    product = Product(1,  "Watch", 150, 10)
    assert product.stock == 10

def test_product_stock_nonnegative():
    product = Product(1,  "Watch", 150, 10)
    with pytest.raises(ValueError):
        product.stock = -1

