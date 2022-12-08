from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.mysql import VARCHAR
from sqlalchemy import Column

from database.models.mixins import MysqlTimestampsMixin, MysqlPrimaryKeyMixin

Base = declarative_base()


class Product(Base, MysqlPrimaryKeyMixin, MysqlTimestampsMixin):
    __tablename__ = 'product'

    name = Column(VARCHAR(200))
    url = Column(VARCHAR(1000))
    price = Column(VARCHAR(20))
    discounted_price = Column(VARCHAR(100))
    image_url = Column(VARCHAR(1000))
    category = Column(VARCHAR(100))
