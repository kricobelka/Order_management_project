from repositories.product_repository import ProductRepository
from product import Product
import pytest


def test_product_existing_by_id(db_connection):

    with db_connection.cursor() as cursor:
            
            cursor.execute("""INSERT INTO products (name, price, stock)
            VALUES (%s, %s, %s)
            RETURNING id, name, price, stock;
            """, ("Server", 1000, 3))

            product_info = cursor.fetchone()
            product_object = Product.from_db_tuple(product_info)

            repository = ProductRepository(cursor)
            product_result = repository.get_product_by_id(product_object)

            assert product_result.product_id == product_info[0]
            assert product_result.product_name == product_info[1]
            assert product_result.price == product_info[2]
            assert product_result.stock== product_info[3]
            

def test_product_nonexisting_by_id(db_connection):

    with db_connection.cursor() as cursor:
        
        repository = ProductRepository(cursor)
        fake_product = Product(product_id = 999, product_name="Fake", price=567, stock=5)

        with pytest.raises(ValueError):
        # or with pytest.raises(ValueError, match="Product is not found") проверяет дополнительно текст исключения
            repository.get_product_by_id(fake_product)