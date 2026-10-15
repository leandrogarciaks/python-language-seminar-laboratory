""" from curses.ascii import HT """
""" from itertools import product
from math import e, prod
import stat """

from fastapi import FastAPI, status, HTTPException
from database import Carts, db_session, Products, Sales
from schema import ProductCreate, ProductResponse, SaleCartAssign, SaleCreate, SaleResponse

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

##############################
######### PRODUCTS ###########
##############################

#
# GET /productos
#
@app.get("/products", status_code=status.HTTP_200_OK)
async def get_product():
    try:
        products = Products.query.all()
        response = {"products": products}
        return response
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"An error occurred while trying to get products: {e}")    

#
# GET /productos/{product_id}
#
@app.get("/products/{product_id}", status_code=status.HTTP_200_OK)
async def get_product(product_id):
    try:
        product = Products.query.get(product_id)

        if not product:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
        
        response = {"product": product}
        return response
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"An error occurred while trying to get product with id {product_id}: {e}")    

#
# POST /productos
#
@app.post("/products", status_code=status.HTTP_201_CREATED)
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
        
        response = {"product": product}
        return response
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"An error occurred while trying to create product: {e}")    

#
# PUT /productos/{product_id}
#
@app.put('/products/{product_id}', status_code=200, response_model=ProductResponse)
async def update_product( product_id: int, producto_data: ProductCreate ):
    try:
        product: Products = Products.query.get(product_id)

        if not product:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not fount.")

        product.name = producto_data.name
        product.price = producto_data.price

        db_session.commit()
        db_session.refresh(product)

        return product

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"An error occurred while trying to create product: {e}")
#
# DELETE /productos/{product_id}
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
        product = Products.query.get(sale_data.product_id)
        
        if not product:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product does not exist")
        
        sale = Sales(
            date = sale_data.date,
            time = sale_data.time,
            id_time = sale_data.id_cart,
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
async def get_sale(sale_id):
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
        product: Products = Products.query.get(sale_data.product_id)

        if not sale:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Sale not fount with id {sale_id}")

        if not product:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Product not fount with id {sale_id}")

        sale.date = sale_data.date
        sale.time = sale_data.time
        sale.quantity = sale_data.quantity
        sale.product_id = sale_data.product_id
        sale.total_price = round(product.price * sale_data.quantity)
        
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
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Sale not fount with id {sale_id}")

        db_session.delete(sale)
        db_session.commit()

        return {
            "message": "Sale delete ok."
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"An error occurred while trying to update sale: {e}")

#
# POST /sales/{sale_id}/cart
# 
@app.post("/carts", status_code=status.HTTP_201_CREATED, response_model=CartCreate)
async def create_cart():
    try:

    except:

#
# POST /sales/{sale_id}/cart
# 
@app.post('/sales/{sale_id}/cart', status_code=status.HTTP_200_OK, response_model=SaleResponse)
async def sale_cart_assign(sale_id: int, sale_data: SaleCartAssign):

    try:
        sale: Sales = Sales.query.get(sale_id)
        
        if not sale:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Sale not fount witch id {sale_id}")

        cart = Carts.query.get(sale_data.id_cart)
        if not cart:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Cart not found id {sale_data.id_cart}")

        if cart.state != "close":
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Only closed carts can be assigned to a sale")

        if cart.sale is None and cart.sale.id != sale_id:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Cart is already assigned to another sale")


        sale.id_cart = sale_data.id_cart

        db_session.commit()
        db_session.refresh(sale)

        return sale
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"An error occurred while trying to update sale: {e}")


    