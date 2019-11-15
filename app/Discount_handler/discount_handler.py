from flask import Blueprint, render_template, abort, jsonify, request
from Database_discount_handler.db_handler import Db_handler as db
from Products_discount.products_discount import Products_discount
import requests

db_handler = db()
product_discount = Products_discount(db_handler)


discount_router = Blueprint('discount_api', 
                                import_name=__name__, 
                                url_prefix='/discounts')

@discount_router.route('/')
def index():
    return "Discounts handler component"


@discount_router.route('/populate')
def populate():
    response = product_discount.populate()
    return jsonify(response)

@discount_router.route('/products/all')
def get_all():
    response = db_handler.find_products_discount(all_products=True)
    return jsonify(response)

@discount_router.route('/products/month_products')
def with_discount():
    response = db_handler.find_products_discount()
    return jsonify(response)

'''

{
	"products":
	[
		{
      "_id": "1", 
      "discount": 0, 
      "user_profile": {
        "1": false, 
        "2": false, 
        "3": false
      }, 
      "valid": false
    }, 
    {
      "_id": "2", 
      "discount": 0, 
      "user_profile": {
        "1": false, 
        "2": false, 
        "3": false
      }, 
      "valid": false
	}]
}
'''
@discount_router.route('/products/alter', methods=['POST'])
def alter():
    data = request.get_json()
    products = data['products']
    print(products)
    response = db_handler.alter_products_discounts(products)

    return jsonify(response)

'''
{
	"id_user": "1036681553",
	"products":
	[
		{
    "_id": "1", 
	  "quantity": 10
    }, 
    {
    "_id": "2", 
	  "quantity": 10
    }]
}
'''
@discount_router.route('/bill', methods=['POST'])
def bill():
    bill = request.get_json()

    id_user = bill['id_user']
    products = bill['products']

    res_get = requests.get('http://fiel.tk' + '/membership/user/profile/id/' + str(id_user))

    status, data = res_get.status_code, res_get.json()
    
    if data['status'] == 'err':
        return { "status": 'err',"err": "user doesn't exist"}
    

    return jsonify(product_discount.bill_discount(data['type'], products))


