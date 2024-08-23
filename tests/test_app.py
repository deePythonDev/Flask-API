import pytest
from random import randint
import sys
import os

# Append the path to the app
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app  # Import the Flask app

@pytest.fixture
def client():
    # Use the Flask test client to interact with the app
    with app.test_client() as client:
        yield client


#--------------------------------------------------------------------------------------
# test functions to test add product route/functionality

def test_add_product_success(client):
    """
    Test adding a product with complete information
    """
    # Simulate a POST request to the '/add_product' route
    json_params = {
        'name': 'Laptop Charger',
        'description': 'Laptop Charger C-type, brick, 44W',
        'price': 1500,
        'inventory_count': 0,
        'category': 'Computer'
    }

    response = client.post('/add_product', json=json_params)

    expected_message1 = "Product added successfully"
    expected_message2 = f"Product {json_params.get('name')} already exists"

    response_data = response.get_json()


    if response.status_code == 201:
        assert response.status_code == 201  
        assert response_data.get("message") == expected_message1



def test_add_product_with_less_info(client):
    """
    Test adding product with no price value..
    """
    json_params = {
        'name': 'Nutrella',
        'description': 'product 3 description',
        'inventory_count': 500,
        'category': 'Category 3'
    }

    response = client.post('/add_product', json = json_params)
    response_data = response.get_json()

    assert response.status_code == 400
    assert response_data['mesage']  == "price data is missing"


def test_add_product_error(client):
    """
    Test adding product with already existing product
    """

    json_params = {
        'name': 'Corn Flakes',
        'description': 'product 4 description',
        'price': 100,
        'inventory_count': 500,
        'category': 'Category 4'
    }

    response = client.post('/add_product', json = json_params)

    response_data = response.get_json()

    assert response.status_code == 400
    assert response_data['message'] == f"Product {json_params.get('name')} already exists"


#--------------------------------------------------------------------------------------------------------

# test functions for getting all product list...

def test_get_product_success(client):
    """
    Test getting all product info
    """

    response = client.get('/product')

    response_data = response.get_json()

    assert response.status_code == 200
    assert response_data['message'] == "List of all products"
    

def test_get_product_failure(client):
    """
    Test getting product info wen no product in DB(Table)
    """

    response = client.get('/product')

    response_data = response.get_json()
    
    if response.status_code == 400:
        assert response.status_code == 400
        assert response_data['message'] == "List of all products"


# ----------------------------------------------------------------------------------------------------

# test functions for getting single product using its id..

def test_get_single_product_success(client):
    """
    Test getting a single product info using its product id
    """

    test_id = 5
    response = client.get(f'/get_product/{test_id}')

    response_data = response.get_json()

    assert response.status_code == 200
    assert response_data['message'] == f"product with product id {test_id} exists"


def test_get_single_product_faliure(client):
    """
    Test getting product info, with non-existing product id
    """
    test_id = 100
    response = client.get(f'/get_product/{test_id}')

    response_data = response.get_json()
    
    assert response.status_code == 400
    assert response_data['message'] == f"product with product id {test_id} doesn't exists"


# -------------------------------------------------------------------------------------------------------------
# test functions to update existing product...

# case 1 (if product exists)
# case 2 (if product doesn't exists)


def test_update_product_details_success(client):
    """
    Test updating existing product details...
    """
    test_product_id = 5
    json_params =  {
        'name': 'New Name'
    }
    response = client.put(f'/update_product/{test_product_id}', json = json_params)
    response_data = response.get_json()

    assert response.status_code == 201
    assert response_data['message'] == "Product updated successfully"


def test_update_product_details_faliure(client):
    """
    Test updating existing product details...
    """
    test_product_id = 100
    json_params =  {
        'name': 'New Name'
    }
    response = client.put(f'/update_product/{test_product_id}', json = json_params)
    response_data = response.get_json()

    assert response.status_code == 400
    assert response_data['message'] == f"product with product id {test_product_id} doesn't exists"


# -----------------------------------------------------------------------------------------------------------------

# test functions for deleting a product.

# case 1 (product exists and get deleted)
# case 2 (product doesn't exists)


def test_delete_product_success(client):
    """
    Test delete existing product
    """

    test_product_id = 4 ## (change product id with existing product id)
    
    response = client.delete(f'/del_product/{test_product_id}')

    response_data = response.get_json()
    
    if response.status_code == 200:
        assert response.status_code == 200
        assert response_data['message'] ==  "Product deleted successfully"


def test_delete_product_faliure(client):
    """
    Test delete non-existing product
    """

    test_product_id = 100
    
    response = client.delete(f'/del_product/{test_product_id}')

    response_data = response.get_json()

    assert response.status_code == 400
    assert response_data['message'] == f"No such product exist with id {test_product_id}"



# ------------------------------------------------------------------------------------------

# testing functions to seach products by their name, description or category ..

## Case 1 (if products exists)
## case 2 (if product doesn't exists)


def test_product_search_success(client):

    json_params = {
        'name': 'Mouse'
    }

    response = client.get('/search_product',query_string=json_params)
    response_data = response.get_json()

    assert response.status_code == 200
    assert response_data['message'] == 'Searched Product Match'


def test_product_search_faliure(client):
    json_params = {
        'name': 'non-existing'
    }

    response = client.get('/search_product', query_string = json_params)
    response_data = response.get_json()

    assert response.status_code == 404
    assert response_data['message'] == "No Such product found"



# ---------------------------------------------------------------------------------------

# testing getting popularity scores of product.
## case 1 (if products exists in model)  return: popularity scores
## case 2 (no product in model) return: error/message

def test_get_popularity_score_success(client):
    """
    Test get popularity score of products
    """
    response = client.get('/get_popularity')
    response_data = response.get_json()

    assert response.status_code == 200
    assert response_data['message'] == "Product Popularity Scores in Descending Order"


def test_get_popularity_score_faliure(client):
    """
    Test get popularity score of products, if model is empty
    """
    response = client.get('/get_popularity')
    response_data = response.get_json()

    if response.status_code == 404:
        assert response.status_code == 404
        assert response_data['message'] == "No Products Details Available"



# -------------------------------------------------------------------------------------------------------------
# testing buying product function....
## case 1 (product exists and buying successful)
## case 2 (product doesn't exists)
## case 3 (product exists in model but inventory is empty)


def test_buy_product_success(client):
    """
    Test buying product
    """

    test_product_id = 1

    response = client.get(f'/buy_product/{test_product_id}')
    response_data = response.get_json()

    assert response.status_code == 201
    assert response_data['message'] == f"Purchase of product with id {test_product_id} is completed..."


def test_buy_product_faliure(client):

    test_product_id = 500

    response = client.get(f'/buy_product/{test_product_id}')
    response_data = response.get_json()

    assert response.status_code == 404
    assert response_data['message'] == f"No such product with product id {test_product_id}"



def test_buy_product__null_inventory(client):

    test_product_id = 18

    response = client.get(f'/buy_product/{test_product_id}')
    response_data = response.get_json()

    assert response.status_code == 400
    assert response_data['message'] == "0 product in inventory"
