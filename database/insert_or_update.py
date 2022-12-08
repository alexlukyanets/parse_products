from sqlalchemy import update
from sqlalchemy.sql import select
from database.models.products import Product, Base

from sqlalchemy.dialects import mysql
from sqlalchemy.dialects.mysql import insert

import sqlalchemy
from database.mysql_connection_string import mysql_connection_string
from items import ProductItem

engine = sqlalchemy.create_engine(mysql_connection_string())
engine.connect()
Base.metadata.create_all(engine)


def select_item(item: ProductItem):
    stmt = select(Product.id).where(Product.name == item.name,
                                    Product.url == item.url,
                                    Product.image_url == item.image_url,
                                    Product.category == item.category)
    result = compile_execute_selection(stmt)
    product_id = result.fetchall()
    if not product_id or len(product_id) != 1:
        return
    return product_id[0]


def compile_execute_selection(stmt, item=None):
    try:
        stmt_compiled = stmt.compile(compile_kwargs={"literal_binds": True}, dialect=mysql.dialect())
    except (TypeError, AttributeError):
        return
    return engine.execute(str(stmt_compiled), tuple(stmt_compiled.params.values()))


def insert_to_db(item: ProductItem):
    inserted_stmt = insert(Product)
    stmt = inserted_stmt.values(item.__dict__)
    compile_execute_selection(stmt, item)


def update_item(item, wine_id):
    item['id'] = wine_id[0]
    stmt = update(Product).where(Product.id == wine_id[0]).values(item)
    compile_execute_selection(stmt)


def insert_or_update(product_item: ProductItem):
    product_id = select_item(product_item)
    if product_id:
        update_item(product_item.__dict__, product_id)
        return False
    insert_to_db(product_item)
    return True
