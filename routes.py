from flask import Blueprint, request, jsonify
from models import Product, db, Category

from sqlalchemy.orm import Session

products_bp = Blueprint('products', __name__)
session: Session = db.session

# route to add new product.....
@products_bp.route('/add_product', methods=['POST'])
def add_product():
    """
    Add a new product
    ---
    tags:
      - Products
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          required:
            - name
            - description
            - price
            - inventory_count
            - category
          properties:
            name:
              type: string
              description: The name of the product
            description:
              type: string
              description: A description of the product
            price:
              type: number
              description: The price of the product
            inventory_count:
              type: integer
              description: The inventory count of the product
            category:
              type: string
              description: The category of the product
    responses:
      201:
        description: Product created successfully
      400:
        description: Invalid input or product already exists
    """
    try:

        if request.method == 'POST':
            data = request.get_json()
            if data:
                category_name = data.get('category','Uncategorized')

                required_values_list = ['name', 'price', 'inventory_count']
                for val in required_values_list:
                    if val not in data.keys():
                        return jsonify({'mesage': f"{val} data is missing"}), 400
                    
                ## what-if product already exists in product table..
                existing_product = Product.query.filter_by(name = data['name']).first()
                if existing_product:
                    return jsonify({
                        "message": f"Product {data['name']} already exists"
                    }), 400

                # Check if the category exists
                category = Category.query.filter_by(name=category_name).first()
                if not category:
                    # If category doesn't exist, create it
                    category = Category(name=category_name)
                    db.session.add(category)
                    db.session.commit()

                # adding new product
                new_product = Product(
                name=data['name'],
                
                description=data['description'],
                price=data['price'],
                inventory_count=data['inventory_count'],
                category= category.name,
                product_sales = data.get("product_sales")
                )
                db.session.add(new_product)
                db.session.commit()

                return jsonify({"message": "Product added successfully",
                                'data': {
                                    'Product Name': new_product.name,
                                    "Product Description": new_product.description,
                                    "Product price":new_product.price,
                                    "Product category": new_product.category
                                }}), 201

        else:
            return jsonify({"message": "bad Request"}), 400
        
    except Exception as e:
        return jsonify({"exception": str(e)})


# get all products..
@products_bp.route('/product', methods = ['GET'])
def products():
    try:
        products = Product.query.all()
        if products:
            result = {
                "message": "List of all products",
                "Data": [{'id': p.id, 'name': p.name} for p in products]
                    }

            return jsonify(result),200
        else:
            return jsonify({
                "message": "No products in product table"
            }), 400
    
    except Exception as e:
        return jsonify({"Exception":str(e)})    
    


# Get a single product by ID
@products_bp.route('/get_product/<int:product_id>', methods=['GET'])
def get_product(product_id):
    """
    Get a single product by its ID
    ---
    tags:
      - Products
    parameters:
      - name: product_id
        in: path
        type: integer
        required: true
        description: The ID of the product to retrieve
    responses:
      200:
        description: Product details retrieved successfully
        schema:
          id: Product
          properties:
            id:
              type: integer
            name:
              type: string
            description:
              type: string
            price:
              type: number
            inventory_count:
              type: integer
            category:
              type: string
      404:
        description: Product not found
    """

    try:
        # product = Product.query.get(product_id)
        product = session.get(Product, product_id)

        if product:
            return jsonify({'message': f"product with product id {product_id} exists",
                            'Data':{
                            "id": product.id,
                            "name": product.name,
                            "description": product.description,
                            "price": product.price}
                            }), 200
        else:
            return jsonify({"message": f"product with product id {product_id} doesn't exists"}), 400
        
    except Exception as e:
        return jsonify({"exception":str(e)})    



# route to update existing product info...
@products_bp.route('/update_product/<int:product_id>', methods = ['PUT'])
def update_product(product_id):
    try:
        # product = Product.query.get(product_id)
        product = session.get(Product, product_id)
        if product:
            data = request.get_json()
            product.name = data.get('name', product.name)
            product.description = data.get('description', product.description)
            product.price = data.get('price', product.price)
            product.inventory_count = data.get('inventory_count', product.inventory_count)
            product.category = data.get('category', product.category)
            product.product_sales = data.get('product_sales', product.product_sales)
            db.session.commit()

            return jsonify({"message": "Product updated successfully"}), 201
        
        else:
            return jsonify({"message": f"product with product id {product_id} doesn't exists"}), 400
    
    except Exception as e:
        return jsonify({"exception":str(e)})    


# Delete a product
@products_bp.route('/del_product/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    try:
        # product = Product.query.get(product_id)
        product = session.get(Product, product_id)
        if product:
            db.session.delete(product)
            db.session.commit()
            return jsonify({"message": "Product deleted successfully",
                            'data': product}), 200
        else:
            return jsonify({"message": f"No such product exist with id {product_id}"}), 400
        
    except Exception as e:
        return jsonify({"exception":str(e)})


# product search by name, description and category ..
@products_bp.route('/search_product', methods = ['GET'])
def search_product():
    
    try: 
        query = Product.query
        name = request.args.get('name')
        description = request.args.get('description')
        category = request.args.get('category')

        if name:
            query = query.filter(Product.name.ilike(f'%{name}%'))
        if category:
            query = query.filter(Product.category.ilike(f'%{category}%'))
        if description:
            query = query.filter(Product.description.ilike(f'%{description}%'))

        products = query.all()
        if products:
            result = {"message": "Searched Product Match"
                    ,"data":[
                    {"id": p.id, "name": p.name, "description": p.description, "price": p.price,
                    "inventory_count": p.inventory_count, "category": p.category,
                    "product_sales": p.product_sales} for p in products]
            }

            return jsonify(result), 200
        
        else:
            return jsonify({'message': "No Such product found"}), 404
        
    except Exception as e:
        return jsonify({"Exception":str(e)})


# get popularity score of all product...
@products_bp.route('/get_popularity', methods = ['GET'])
def get_populatity_score():
    try:
        products = Product.query.all()

        if not products:
            return jsonify({
                            "message": "No Products Details Available"
                             }), 404

        product_sales_dict = {}
        product_popularity_scores = {}

        for product in products:
            product_sales_dict[product.name] = product.product_sales

        
        # calculate popularity in range 1 to 10...
        min_sales =  min(product_sales_dict.values())
        max_sales =  max(product_sales_dict.values())

        if max_sales == min_sales:  # Handle edge case where all products have same sales
            popularity_score =  10  # Or any fixed score, depending on your preference
            product_popularity_scores = dict().fromkeys(product_sales_dict.keys(), 10)

        else:
            # implementing min-max algorithm to range the popularity score between 1 to 10.
            for product, sales in product_sales_dict.items():
                popularity_score = 1 + (sales - min_sales) * (10 - 1) / (max_sales - min_sales)
                product_popularity_scores[product] = popularity_score

            # Sort by values in descending order and return a dictionary
            # sorted_by_values = {
            #     "Popularity Score": dict(sorted(product_popularity_scores.items(), 
            #                                     key=lambda item: item[1], reverse=True))
            # }

            sorted_by_values = sorted(product_popularity_scores.items(), 
                                                key=lambda item: item[1], reverse=True)

        return jsonify({"message": "Product Popularity Scores in Descending Order",
                        "data": sorted_by_values}), 200
    
    except Exception as e:
        return jsonify([{"exception":str(e)}])



# buy product...
@products_bp.route('/buy_product/<int:product_id>', methods = ['GET'])
def buy_product(product_id):
    try:
        # quantity = request.args.get('quantity') # passed as params
        # if not quantity:
        #     quantity = 1
        quantity = 1

        # product = Product.query.get(product_id)
        product = session.get(Product, product_id)
        if product:
            product_inventory = product.inventory_count
            if product_inventory <= 0:
                return jsonify({
                    "message": "0 product in inventory"

                }), 400
            
            product_inventory -= quantity
            
            product.inventory_count = product_inventory
            product.product_sales += quantity
            db.session.commit()

            return jsonify({'message': f"Purchase of product with id {product.id} is completed..."}), 201
        
        else:
            return jsonify({'message':f"No such product with product id {product_id}"}), 404
        
    except Exception as e:
        return jsonify({"exception":str(e)})
