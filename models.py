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
    id = db.Column(db.Integer, primary_key=True, autoincrement=False)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    address = db.Column(db.String(255))
    state = db.Column(db.String(20))
    zip = db.Column(db.String(10))


class Product(Base):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True, autoincrement=False)
    name = db.Column(db.String(100))


class Order(Base):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    customer_id = db.Column(db.Integer, ForeignKey("customers.id"))
    product_id = db.Column(db.Integer, ForeignKey("products.id"))
    price = db.Column(db.Float)
    status = db.Column(db.String(10))
    date = db.Column(db.DateTime)


Base.metadata.create_all(bind=engine)