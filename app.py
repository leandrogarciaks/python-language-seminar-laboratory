from tkinter import E

from fastapi import FastAPI, status, HTTPException
from database import Carts, db_session, Products, Sales
from schema import (
    CartCreate, CartResponse, ProductCreate, ProductResponse,
    SaleCreate, SaleCartAssign, SaleResponse,
)

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

##############################
######### PRODUCTS ###########
##############################

#
# GET /products
#
@app.get("/products", status_code=status.HTTP_200_OK, response_model=list[ProductResponse])
async def get_products():
    try:
        products = Products.query.all()
        return products
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"An error occurred while trying to get products: {e}")

#
# GET /products/{product_id}
#
@app.get("/products/{product_id}", status_code=status.HTTP_200_OK, response_model=ProductResponse)
async def get_product(product_id: int):
    try:
        product = Products.query.get(product_id)

        if not product:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")

        return product
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"An error occurred while trying to get product with id {product_id}: {e}")

#
# POST /products
#
@app.post("/products", status_code=status.HTTP_201_CREATED, response_model=ProductResponse)
async def create_product(product_data: ProductCreate):
    try:
        product = Products.query.filter_by(name=product_data.name).first()

        if product:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Product already exists")

        product = Products(
            name=product_data.name,
            price=product_data.price
        )

        db_session.add(product)
        db_session.commit()
        db_session.refresh(product)

        return product
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"An error occurred while trying to create product: {e}")

#
# PUT /products/{product_id}
#
@app.put('/products/{product_id}', status_code=200, response_model=ProductResponse)
async def update_product(product_id: int, producto_data: ProductCreate):
    try:
        product: Products = Products.query.get(product_id)

        if not product:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found.")

        product.name = producto_data.name
        product.price = producto_data.price

        db_session.commit()
        db_session.refresh(product)

        return product

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"An error occurred while trying to update product: {e}")

#
# DELETE /products/{product_id}
#
@app.delete('/products/{product_id}', status_code=200)
async def delete_product(product_id: int):

    try:
        product: Products = Products.query.get(product_id)

        if not product:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found.")

        db_session.delete(product)
        db_session.commit()

        return {
            "message": "El producto fue eliminado con exito"
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"An error occurred while trying to delete product: {e}")

##############################
########## SALES #############
##############################

#
# POST /sales
#
@app.post("/sales", status_code=status.HTTP_201_CREATED, response_model=SaleResponse)
async def create_sale(sale_data: SaleCreate):
    try:
        cart = Carts.query.get(sale_data.id_cart)

        if not cart:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Cart not found id {sale_data.id_cart}")

        if cart.state != "closed":
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Only closed carts can be assigned to a sale")

        if cart.sale is not None:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Cart is already assigned to another sale")

        sale = Sales(
            date_sale=sale_data.date_sale,
            time_sale=sale_data.time_sale,
            id_cart=sale_data.id_cart,
        )

        db_session.add(sale)
        db_session.commit()
        db_session.refresh(sale)

        return sale
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"An error occurred while trying to create sale: {e}")

#
# GET /sales
#
@app.get("/sales", status_code=status.HTTP_200_OK, response_model=list[SaleResponse])
async def get_sales():
    try:
        sales = Sales.query.all()
        return sales
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"An error occurred while trying to get sales: {e}")

#
# GET /sales/{sale_id}
#
@app.get("/sales/{sale_id}", status_code=status.HTTP_200_OK, response_model=SaleResponse)
async def get_sale(sale_id: int):
    try:
        sale = Sales.query.get(sale_id)

        if not sale:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Sale not found")

        return sale
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"An error occurred while trying to get sale with id {sale_id}: {e}")

#
# PUT /sales/{sale_id}
#
@app.put('/sales/{sale_id}', status_code=200, response_model=SaleResponse)
async def update_sale(sale_id: int, sale_data: SaleCreate):
    try:
        sale: Sales = Sales.query.get(sale_id)

        if not sale:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Sale not found with id {sale_id}")

        cart = Carts.query.get(sale_data.id_cart)

        if not cart:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Cart not found id {sale_data.id_cart}")

        if cart.state != "closed":
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Only closed carts can be assigned to a sale")

        if cart.sale is not None and cart.sale.id != sale_id:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Cart is already assigned to another sale")

        sale.date_sale = sale_data.date_sale
        sale.time_sale = sale_data.time_sale
        sale.id_cart = sale_data.id_cart

        db_session.commit()
        db_session.refresh(sale)

        return sale

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"An error occurred while trying to update sale: {e}")

#
# DELETE /sales/{sale_id}
#
@app.delete('/sales/{sale_id}', status_code=status.HTTP_200_OK)
async def delete_sale(sale_id: int):
    try:
        sale: Sales = Sales.query.get(sale_id)

        if not sale:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Sale not found with id {sale_id}")

        db_session.delete(sale)
        db_session.commit()

        return {
            "message": "Sale delete ok."
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"An error occurred while trying to delete sale: {e}")

#
# POST /sales/{sale_id}/cart
#
@app.post('/sales/{sale_id}/cart', status_code=status.HTTP_200_OK, response_model=SaleResponse)
async def sale_cart_assign(sale_id: int, sale_data: SaleCartAssign):

    try:
        sale: Sales = Sales.query.get(sale_id)

        if not sale:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Sale not found with id {sale_id}")

        cart = Carts.query.get(sale_data.id_cart)
        if not cart:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Cart not found id {sale_data.id_cart}")

        if cart.state != "closed":
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Only closed carts can be assigned to a sale")

        if cart.sale is not None and cart.sale.id != sale_id:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Cart is already assigned to another sale")

        sale.id_cart = sale_data.id_cart

        db_session.commit()
        db_session.refresh(sale)

        return sale

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"An error occurred while trying to update sale: {e}")

##############################
########## CARTS #############
##############################

# POST /carritos LISTO
# GET /carritos LISTO
# GET /carritos/{id} LISTO
# PUT /carritos/{id}
# DELETE /carritos/{id}
# POST /carritos/{id}/productos
# DELETE /carritos/{id}/productos/{id_producto}

#
# POST /carts
#
@app.post("/carts", status_code=status.HTTP_201_CREATED, response_model=CartResponse)
async def create_cart(cart_data: CartCreate):
    try:
        cart = Carts(
            creation_date=cart_data.creation_date,
            state=cart_data.state
        )

        db_session.add(cart)
        db_session.commit()
        db_session.refresh(cart)

        return cart

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"An error occurred while trying to create cart: {e}")

#
# GET /carts
#
@app.get('/carts', status_code=status.HTTP_200_OK, response_model=list[CartResponse])
async def get_carts():
    try:
        carts = Carts.query.all()

        return carts
    
    except Exception as e: 
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"An error occurred while trying to get cart: {e}")

#
# GET /carts/{id}
#
@app.get('/carts/{cart_id}', status_code=status.HTTP_200_OK, response_model=CartResponse)
async def get_cart(cart_id: int):
    try:

        cart = Carts.query.get(cart_id)

        if not cart:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Not found cart id {cart_id}")

        return cart

    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"An error occurred while trying to get cart_id {e}")

#
# PUT /carritos/{id}
#

    