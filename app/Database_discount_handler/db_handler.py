from pymongo import MongoClient
from bson.objectid import ObjectId

class Db_handler:
    def __init__(self):
        self.db, self.discounts_collection = self.connection()
        
    def connection(self):
        client = MongoClient('3.227.75.85', 80)
        db = client['losFieles']
        colllection = db['discounts']

        return db, colllection
    '''
        [{
            p_id, -> product
            
            discount, -> 0 .. 1

            user_profile = {
                1: True | Flase,
                2: True | Flase,
                3: True | Flase
            }
            valid -> True | Flase
        },
        ...
        ]
    
    '''
    def associated_discounts(self,products_list):

        products_to_insert = []

        for product_to_check in products_list:
            check = self.discounts_collection.find_one({'_id': product_to_check['_id']})
            
            to_insert ={
                '_id': str(product_to_check['_id']),
                'discount': product_to_check['discount'],
                'user_profile': product_to_check['user_profile'],
                'valid': product_to_check['valid']
            }

            if not(check):
                products_to_insert.append(to_insert)
            
        if len(products_to_insert) > 0:
            self.discounts_collection.insert_many(products_to_insert)

        response = {
            'status' : 'ok',
            'products_to_insert': products_to_insert
        }

        return response

    '''
        [{
            _id, -> product
            
            discount, -> 0 .. 1

            user_profile = {
                1: True | Flase,
                2: True | Flase,
                3: True | Flase
            }
            valid -> True | Flase
        },
        ...
        ]
    
    '''
    def alter_products_discounts(self, products_list):
        #Only one product could have a discount and be valid true
        new_products_counter, update_products_counter = 0,0
        new_products_list, update_products_list = [], []

        for product_to_check in products_list:
            product = self.discounts_collection.find_one({
                '_id':str(product_to_check['_id']),
            })

            if product:
                to_update = {
                    'discount': product_to_check['discount'],
                    'user_profile': product_to_check['user_profile'],
                    'valid': product_to_check['valid']
                }
                self.discounts_collection.update_one({'_id':product['_id']},{"$set":to_update})

                update_products_counter += 1
                update_products_list.append(to_update)

            else:
                to_insert ={
                    '_id': product_to_check['_id'],
                    'discount': product_to_check['discount'],
                    'user_profile': product_to_check['user_profile'],
                    'valid': product_to_check['valid']
                }
                self.discounts_collection.insert_one(to_insert)
                new_products_counter += 1
                new_products_list.append(to_insert)

        response = {
            'status' : 'ok',
            'new_products': {
                'new_products_counter': new_products_counter,
                'new_products_list':new_products_list
            },
            'updated_products': {
                'update_products_counter': update_products_counter,
                'update_products_list':update_products_list
            }
        }

        return response

    def use_discounts(self):
        pass

    def find_products_discount(self,all_products=False):
        products_discount = []
        condition = {}

        if not(all_products):
            condition = {'valid':True}    

        for product in self.discounts_collection.find(condition):
            #product.pop('_id')
            product['_id'] = str(product['_id'])
            products_discount.append(product)
        
        response = {
            "status":"ok",
            "products_discount": products_discount
        }

        return response
