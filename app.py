from fastapi import FastAPI, HTTPException, status
from data_base import Product, Sale, db_session, Base, product_data
from models import CreateProduct, UpdateProduct

app = FastAPI()

@app.get('/hello-word')
def hello_word():
    return 'Hello word!!'

@app.get('/products')
def list_products():
    products = Product.query.all()
    return [vars(product) for product in products]

@app.get('/products/{id_product}')
def get_product(id_product: int):
    product = Product.query.get(id_product)
    if product is None:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return vars(product)

@app.post("/products", status_code=status.HTTP_201_CREATED)
def create_product(product_data: CreateProduct):
    new_product = Product(
        name = product_data.name,
        price = product_data.price
    )

    db_session.add(new_product)

    try:
        db_session.commit()
        db_session.refresh(new_product)
    except:
        db_session.rollback()
        raise HTTPException(status_code=400, detail="Error al crear un producto")

    return vars(new_product)

@app.put('/products/{id_product}')
def modify_products( id_product: int, product_data: UpdateProduct ):
    product = Product.query.get(id_product)

    if product is None:
        raise HTTPException(status_code=404, detail="Producto no encontrado")

    product.name = product_data.name if product_data.name is not None else product.name
    product.price = product_data.price if product_data.price is not None else product.price

    db_session.commit()
    db_session.refresh(product)

    return vars(product)

@app.delete('/products/{id_product}')
def delete_product( id_product: int ):
    product = Product.query.get(id_product)

    if product is None:
        raise HTTPException(status_code=404, detail="Producto no encontrado")

    db_session.delete(product)
    db_session.commit()
    return {"Ok": True}