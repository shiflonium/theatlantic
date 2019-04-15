from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, ForeignKey
from app import db


engine = create_engine('sqlite:///atlantic.db', echo=True)
db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()


class Customer(Base):
    __tablename__ = 'customers'

    def __init__(self, id, first_name, last_name, address, state, zip):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.address = address
        self.state = state
        self.zip = zip

    id = db.Column(db.Integer, primary_key=True, autoincrement=False)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    address = db.Column(db.String(255))
    state = db.Column(db.String(20))
    zip = db.Column(db.String(10))


class Product(Base):
    __tablename__ = 'products'

    def __init__(self, id, name):
        self.id = id
        self.name = name

    id = db.Column(db.Integer, primary_key=True, autoincrement=False)
    name = db.Column(db.String(100))


class Order(Base):
    __tablename__ = 'orders'

    def __init__(self, customer_id, product_id, price, status, date):
        self.customer_id = customer_id
        self.product_id = product_id
        self.price = price
        self.status = status
        self.date = date


    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    customer_id = db.Column(db.Integer, ForeignKey("customers.id"))
    product_id = db.Column(db.Integer, ForeignKey("products.id"))
    price = db.Column(db.Float)
    status = db.Column(db.String(10))
    date = db.Column(db.DateTime)


Base.metadata.create_all(bind=engine)