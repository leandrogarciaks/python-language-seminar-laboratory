from sqlalchemy import create_engine, Column, Integer, String, Float, Date, Time, ForeignKey
from sqlalchemy.orm import scoped_session, sessionmaker, relationship, declarative_base


engine = create_engine("sqlite:///database.db")
db_session = scoped_session(sessionmaker(bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()

class Products(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    price = Column(Float, nullable=False)

    cart_items = relationship("ProductCart", back_populates="product")

class Sales(Base):
    __tablename__ = "sales"

    id = Column(Integer, primary_key=True)
    date_sale = Column(Date, nullable=False)
    time_sale = Column(Time, nullable=False)
    id_cart = Column(Integer, ForeignKey('carts.id'), unique=True, nullable=False)
    id_customer = Column(Integer, ForeignKey('customer.id'), nullable=False)

    @property
    def total_price(self):
        total = 0 
        for item in self.cart.products:
            total += item.product.price * item.quantity
        return total

    cart = relationship("Carts", back_populates="sale")
    customer = relationship("Customer", back_populates="sales")

class Carts(Base):
    __tablename__ = "carts"

    id = Column(Integer, primary_key=True, autoincrement=True)
    creation_date = Column(Date, nullable=False)
    state = Column(String, nullable=False)

    sale = relationship("Sales", back_populates="cart", uselist=False)
    products = relationship("ProductCart", back_populates="cart", cascade="all, delete-orphan")

class ProductCart(Base):
    __tablename__ = "product_cart"

    id = Column(Integer, primary_key=True, autoincrement=True)
    id_cart = Column(Integer, ForeignKey('carts.id'), nullable=False)
    id_product = Column(Integer, ForeignKey('products.id'), nullable=False)
    quantity = Column(Integer, nullable=False)

    product = relationship("Products", back_populates="cart_items")
    cart = relationship("Carts", back_populates="products")

class Customer(Base):
    __tablename__= 'customer'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    lastname = Column(String, nullable=False)
    dni = Column(Integer, nullable=False, unique=True)

    sales = relationship("Sales", back_populates="customer")


Base.metadata.create_all(engine, Base.metadata.tables.values(), checkfirst=True)