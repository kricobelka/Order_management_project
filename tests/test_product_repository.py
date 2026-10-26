from repositories.product_repository import ProductRepository
from product import Product
import pytest
from decimal import Decimal, InvalidOperation
from psycopg.errors import CheckViolation
from notFoundError import NotFoundError


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


def test_added_product_iscorrect(db_connection):
     
     with db_connection.cursor() as cursor:
        product_object = Product(product_id=None, product_name="Laptop", price=Decimal("10000.50"), stock=7)

        repository = ProductRepository(cursor)
        product_result = repository.add_new_product(product_object)

        assert product_result.product_id is not None
        assert product_result.product_id > 0

        assert type(product_result.product_name) is str
        assert isinstance(product_result.price, Decimal)  
        assert type(product_result.stock) is int

        assert product_result.price >= 0
        assert product_result.stock >= 0



def test_updated_product_correctly(db_connection):

    with db_connection.cursor() as cursor:
        cursor.execute("""INSERT INTO products (name, price, stock)
         VALUES (%s, %s, %s)
         RETURNING id;
         """, ("Phone", 3500, 6))

        product_id = cursor.fetchone()[0]

        repository = ProductRepository(cursor)
        info_to_change = "price"
        new_price = 3600

        repository.update_product_information(product_id=product_id, info_to_change=info_to_change,new_value=new_price)

        cursor.execute("""SELECT name, price, stock
                            FROM products
                            WHERE id = %s;
                            """, (product_id, ))

        price = cursor.fetchone()[1]

        assert price == new_price

@pytest.mark.parametrize("info_to_change", [
        ("nam"),
        ("pric"),
        ("st")
])

def test_updated_product_incorrectly(info_to_change, db_connection):
    with db_connection.cursor() as cursor:
        cursor.execute("""INSERT INTO products (name, price, stock)
        VALUES (%s, %s, %s)
        RETURNING id;
        """, ("Phone", 3500, 6))
    
        product_id = cursor.fetchone()[0]
        repository = ProductRepository(cursor)

        with pytest.raises(KeyError):
            repository.update_product_information(product_id, info_to_change, new_value=3600)

def test_updated_product_id_notfound(db_connection):
    with db_connection.cursor() as cursor:
        repository = ProductRepository(cursor)
        with pytest.raises(NotFoundError):
            repository.update_product_information(product_id=999, info_to_change="price", new_value=500)


@pytest.mark.parametrize("info_to_change, invalid_value", [
    ("price", Decimal("-0.01")),
    ("stock", -1)
])

def test_updated_product_priceandstock_checkviolation(info_to_change, invalid_value, db_connection):
    with db_connection.cursor() as cursor:
        cursor.execute("""INSERT INTO products (name, price, stock)
                        VALUES (%s, %s, %s)
                        RETURNING id;
                        """, ("Computer mouse", 85, 10))
        
        added_product_id = cursor.fetchone()[0]

        with pytest.raises(CheckViolation):
            with db_connection.transaction():
                cursor.execute(f"""UPDATE products SET {info_to_change} =%s
                                WHERE id = %s""", (invalid_value, added_product_id)
                )
        

@pytest.mark.parametrize("info_to_change, new_value", 
[
    ("price", Decimal("-0.01")),
    ("stock", -1)
])

def test_updated_product_priceandstock_valueerror(info_to_change, new_value, db_connection):
    with db_connection.cursor() as cursor:
        cursor.execute("""INSERT INTO products (name, price, stock)
                                VALUES (%s, %s, %s)
                                RETURNING id;
                                """, ("Computer mouse", 85, 10))
                
        added_product_id = cursor.fetchone()[0]
        repository = ProductRepository(cursor)

        with pytest.raises(ValueError):
            repository.update_product_information(added_product_id, info_to_change, new_value)

def test_searched_product_byname(db_connection):
    with db_connection.cursor() as cursor:
        cursor.execute("""INSERT INTO products (name, price, stock)
                        VALUES (%s, %s, %s);
        """, ("SSD", Decimal("600.10"), 14))

        repository = ProductRepository(cursor)

        necessary_name = "SSD"

        found_product = repository.search_product_by_name(necessary_name)

        assert found_product.product_name == necessary_name
        assert isinstance(found_product, Product)


def test_searched_product_byname_name_notfound(db_connection):
    with db_connection.cursor() as cursor:
            cursor.execute("""INSERT INTO products (name, price, stock)
                            VALUES (%s, %s, %s);
            """, ("SSD", Decimal("600.10"), 14))
    
            repository = ProductRepository(cursor)
            fake_product_name = "Fakename"

            with pytest.raises(NotFoundError):
                repository.search_product_by_name(fake_product_name)


def test_searched_product_byname_name_incorrect(db_connection):
    with db_connection.cursor() as cursor:
            cursor.execute("""INSERT INTO products (name, price, stock)
                            VALUES (%s, %s, %s);
            """, ("SSD", Decimal("600.10"), 14))
    
            repository = ProductRepository(cursor)
            fake_product_name = 25432

            with pytest.raises(ValueError):
                repository.search_product_by_name(fake_product_name)

        


