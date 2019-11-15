import requests

class Products_discount:
    def __init__(self,db):
        self.fake_POS = 'http://3.86.32.97'
        self.myDB = db
        pass
    
    def populate(self):
        res_get = requests.get(self.fake_POS + '/posts')
        
        status, data = res_get.status_code, res_get.json()
        print(data)
        new_data = []

        for product in data:
            product_to_register = {
                '_id': str(product['id']),
                'discount': 0,
                'user_profile': {
                    '1': False,
                    '2': False,
                    '3': False
                },
                'valid': False    
            }
            new_data.append(product_to_register)
        
        print  (new_data)
        return self.myDB.associated_discounts(new_data)
    
    '''
	[
		{
      "_id": "1", 
	  "cuantity": 10
    }, 
    {
      "_id": "2", 
	  "cuantity": 10
    }]


    returns 
    [
		{
      "_id": "1", 
	  "quantity": 10,
      "discount": X,
      "to_pay" : Y
    }, 
    {
      "_id": "2", 
	  "quantity": 10,
      "discount": X,
      "to_pay" : Y

    }]

    '''
    def bill_discount (self, user_profile, products_bill):
        result = []
        with_discount = self.myDB.find_products_discount(all_products=True)['products_discount']
        #print(with_discount)
        for product in products_bill:
            for products_with_dis in with_discount:
                #print(products_with_dis)
                if product['_id'] == products_with_dis['_id']:

                    res_get = requests.get(self.fake_POS + '/posts/' + str(product['_id']))
                    status, data = res_get.status_code, res_get.json()

                    print(products_with_dis)
                    
                    new_bill_product = {
                        '_id':product['_id'] ,
                        'quantity':product['quantity'],
                        'discount': 0,
                        'price':data['price'],
                        'to_pay': data['price'] * product['quantity']
                    }
                    
                    if products_with_dis['user_profile'][str(user_profile)] and products_with_dis['valid']:
                        new_bill_product['discount'] = products_with_dis['discount']
                        new_bill_product['to_pay'] = (data['price'] - (data['price'] * new_bill_product['discount']))* product['quantity']
                    
                    result.append(new_bill_product)

        return {'status':'ok', 'bill': result}
        





    
        

