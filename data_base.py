from sqlalchemy import create_engine, Column, Integer, String, Float, Date, Time, ForeignKey
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('sqlite:///data_base.db', echo=True)
Base = declarative_base()
db_session = scoped_session(sessionmaker(bind=engine))
Base.query = db_session.query_property()

class Product(Base):
    __tablename__= 'product'
    id = Column(Integer, autoincrement=True, primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    price = Column(Float, nullable=False)

class Sale(Base):
    __tablename__ = 'sale'
    id = Column(Integer, autoincrement=True, primary_key=True, nullable=False)
    date = Column(Date, nullable=False)
    hour = Column(Time, nullable=False)
    id_product = Column(Integer, ForeignKey('product.id'),nullable=False)
    amount = Column(Integer, nullable=False)
    total_price = Column(Float, nullable=False)

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

new_products = []

product_data = [
    ("Esponja", 11.1),
    ("Arroz", 300.0),
    ("Detergente", 20.2),
    ("Fideos", 250.0),
    ("Aceite", 850.0),
    ("Azúcar", 400.0),
    ("Yerba", 1200.0),
    ("Jabón", 350.0),
    ("Lavandina", 280.0),
    ("Papel higiénico", 950.0),
]

for name, price in product_data:
    product = Product(name = name, price = price)
    new_products.append(product)

session.add_all(new_products)
session.commit()