
# to add a new product....

POST: http://localhost:5000/add_product
```json
{
        "name": "Pen",
        "description": "Study Stationary",
        "price": 50,
        "inventory_count": 100,
        "category": "stationary",
        "product_sales": 9
}
```

# to get all the products...

GET: http://localhost:5000/product


# to get specific product based using its id..

 GET: http://localhost:5000/get_product/<product_id>
 
 
 # update existing product info
 
  PUT :http://localhost:5000/update_product/<product_id>
 ```json
 {
        "name": "LCD Monitor",
        "description": "Small Light Torch",
        "price": 100,
        "inventory_count": 200,
        "category": "Home Essentials",
        "product_sales": 0
}
```

# search product using its name, description , category...

GET : http://localhost:5000/search_product/?category=Computer


# delete product...
 DELETE: http://localhost:5000/del_product/<product_id>
 
 # to get the popularity of product...
 GET: http://localhost:5000/get_popularity
 
 
 # to purchase a product...
 
 GET: http://localhost:5000/buy_product/<product_id>
