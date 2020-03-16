from flask import Flask, request, jsonify
from flask_restplus import Api, Resource, fields
from werkzeug.contrib.fixers import ProxyFix
from db import connection, execute_query, execute_read_query
app = Flask(__name__)

import os
import json

# init app 
app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app)
api = Api(app, version='1.0', title='Product Management API',
    description='A Product Management API',
)


basedir = os.path.abspath(os.path.dirname(__file__))


productRoutes = api.namespace('product-management/api', description='Product operations')


class ProductModel:
  def __init__(self, name, description, price, qty):
    self.name = name
    self.description = description
    self.price = price
    self.qty = qty


product = api.model('Product', {
    'id': fields.Integer(readonly=True, description='The Product unique identifier'),
    'name': fields.String(required=True, description='The name of the product'),
    'description': fields.String(required=True, description='The description of the product'),
    'price': fields.Float(required=True, description='The price of the product'),
    'qty': fields.Integer(required=True, description='the quantity of the product'),
})


@productRoutes.route('/products')
class ProductsList(Resource):
	def get(self):
		''' Get All Products'''
		all_products_query = "SELECT * from products"
		products = execute_read_query(all_products_query)
		productsList = []
		for product in products:
			print(products)
			productsList.append(vars(ProductModel(product[1],product[2],product[3],product[4])))
		return productsList, 200

@productRoutes.route('/product/<int:id>')
class Products(Resource):
	def get(self,id):
		''' Get a single product based on ID'''
		single_product_query = "SELECT * from products WHERE id={}".format(id)
		product = execute_read_query(single_product_query)
		if(product == []):
			return "There is no product with id no. {}".format(id), 404
		else:
			return product, 200

	def delete(self,id):
		''' Delete a single product based on ID'''
		single_product_query = "SELECT * from products WHERE id={}".format(id)
		product = execute_read_query(single_product_query)
		if(product == []):
			return "There is no product with id no. {}".format(id), 404
		else:
			delete_product_query = "DELETE FROM products WHERE id={}".format(id)
			delete_product = execute_query(delete_product_query)
			return "Product with id no. {} is deleted.".format(id), 204


	@productRoutes.expect(product)
	def put(self,id):
		''' Update a single product based on ID'''
		single_product_query = "SELECT * from products WHERE id={}".format(id)
		product = execute_read_query(single_product_query)
		if(product == []):
			return "There is no product with id no. {}".format(id), 404
		else:
			data = api.payload 
			new_name = data["name"]
			new_description = data["description"]
			new_price = data["price"]
			new_qty = data["qty"]

			update_product_query = "UPDATE products SET name='{}', description='{}', price={}, qty={} WHERE id={}".format(new_name, new_description, new_price, new_qty, id)
			update_product = execute_read_query(update_product_query)
			return "Product updated", 200


# Run Server
if __name__ == '__main__':
	app.run(debug=True)