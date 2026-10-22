from itertools import product
from os import name

from fastapi import FastAPI, status, HTTPException
from database import Carts, Customer, ProductCart, db_session, Products, Sales
from schema import (
    CartCreate, CartItemResponse, CartProductAdd, CartResponse, CartUpdate, CustomerCreate, CustomerResponse, ProductCreate, ProductResponse,
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
            id_customer = sale_data.id_customer
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
        sale.id_customer = sale_data.id_customer

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

#
# GET /sales/recent/{recent_sales}
#
@app.get('/sales/recent/{recent_sales}', status_code=status.HTTP_200_OK, response_model=list[SaleResponse])
async def get_recent_sales( recent_sales:int ):

    try:
        if recent_sales <= 0:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
            detail="Recente Sale no is posible number negative or cero.")
        
        sales: Sales = Sales.query.order_by(Sales.id.desc()).limit(recent_sales).all()

        if not len(sales):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
            detail="Not found sales")


        return sales

    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"An error occurred while trying to update sale: {e}")
    

##############################
########## CARTS #############
##############################

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
@app.put("/cart/{cart_id}", status_code=status.HTTP_200_OK, response_model=CartResponse)
async def update_cart(cart_id: int, cart_data: CartUpdate):

    try:

        cart: Carts = Carts.query.get(cart_id)

        if not cart:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
            detail="Not found id cart")

        if cart.sale:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
            detail="An error ocurred conflict. Not modifity sale exists")

        cart.creation_date = cart_data.creation_date
        cart.state = cart_data.state

        db_session.commit()
        db_session.refresh(cart)

        return cart

    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail=f"An error occurred while trying to get cart_id {e}")

#
# DELETE /carts/{cart_id}
#
@app.delete('/carts/{cart_id}')
async def delete_cart(cart_id: int):

    try:
        cart: Carts = Carts.query.get(cart_id)

        if not cart:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
            detail="Not found cart_id.")
        
        if cart.sale:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
            detail="Cart associated with sale, can't delete cart id.")

        db_session.delete(cart)
        db_session.commit()
            
        return {"message": "Delete cart successful"}
    
    except HTTPException:
        raise

    except Exception as e:
            db_session.rollback()
            
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while trying to delete cart_id {e}")

#
# POST /carts/{id}/products
#
@app.post('/carts/{cart_id}/products', status_code=status.HTTP_200_OK, response_model=CartItemResponse)
async def add_products_in_cart( cart_id: int, data_cart_product: CartProductAdd):

    try:

        cart: Carts = Carts.query.get(cart_id)

        if not cart:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
            detail="Not found cart id.")

        if cart.sale:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
            detail="Cart associated with sale, can't create card id.")

        if cart.state != 'open':
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
            detail="Cart id as state = 'open', not assiciated with this state.")

        product: Products = Products.query.get(data_cart_product.id_product)

        if not product:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
            detail="Not found product.")

        cart_item: ProductCart = None

        for item in cart.products:
            if item.id_product == product.id:
                cart_item = item
                break

        if not cart_item:
            cart_item = ProductCart(
                id_cart = cart.id,
                id_product = data_cart_product.id_product,
                quantity = data_cart_product.quantity,
            )
        else:
            cart_item.quantity = cart_item.quantity + data_cart_product.quantity

        db_session.add(cart_item)
        db_session.commit()
        db_session.refresh(cart_item)

        return cart_item

    except HTTPException:
        raise

    except Exception as e:
        db_session.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail=f"An error occurred while trying to create cart_id {e}")

#
# DELETE /carts/{cart_id}/products/{product_id}
#
@app.delete('/carts/{cart_id}/products/{product_id}', status_code=status.HTTP_200_OK)
async def delete_producto_cart( cart_id: int, product_id: int ):

    try:
        cart: Carts = Carts.query.get(cart_id)
        product: Products = Products.query.get(product_id)

        if not cart:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                detail="An not found cart.")

        if cart.state == 'closed':
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                detail="Can't delete for car es closed.")

        if not product:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                detail="An not found product.")

        item_product: ProductCart = None

        for item in cart.products:
            if item.id_product == product_id and item.id_cart == cart_id:
                item_product = item

        if not item_product:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                detail="Not found item product for delete.")


        db_session.delete(item_product)
        db_session.commit()

        return  {
            "message": "Delete with exist."
        }

    except HTTPException:
        raise

    except Exception as e:
            db_session.rollback()
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while trying to create cart_id {e}")

##############################
########## CUSTOMER ##########
##############################

#
# post /customers
#
@app.post('/customers', status_code=status.HTTP_201_CREATED, response_model=CustomerResponse)
async def create_user(customer_data: CustomerCreate):

    try:

        customer: Customer = Customer.query.filter_by( dni = customer_data.dni ).first()
        
        if customer:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
            detail="Customer already exists with dni.")
    
        customer = Customer (
            name = customer_data.name,
            lastname = customer_data.lastname,
            dni = customer_data.dni
        )
    
        db_session.add(customer)
        db_session.commit()
        db_session.refresh(customer)
    
        return customer

    except HTTPException:
        raise

    except Exception as e:
        db_session.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail=f"An error occurred while trying to create cart_id {e}")

#
# get /customers
#
@app.get('/customers',status_code=status.HTTP_200_OK, response_model=list[CustomerResponse])
async def get_customers():

    try:

        customer: Customer = Customer.query.all()
        
        return customer

    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail=f"An error occurred while trying to create cart_id {e}")
    