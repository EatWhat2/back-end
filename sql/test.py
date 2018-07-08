import pymysql, traceback, datetime, json

settings = dict()

settings['db_host'] =  'localhost'
settings['db_user'] =  'root'
settings['db_password'] = '89045095'
settings['db_database'] = 'eatwhat'

def query(sql, *args):
  try:
    db = pymysql.connect(host = settings['db_host'], 
                     user = settings['db_user'], 
                     passwd = settings['db_password'], 
                     db = settings['db_database'],
                     charset='utf8')
    cursor = db.cursor()
    if len(args) != 0:
      cursor.execute(sql, args)
    else:
      cursor.execute(sql)
    results = cursor.fetchall()
    db.close()
    return results
  except Exception as e:
    print(traceback.format_exc(e))

def insert_update(sql, *args):
  try:
    db = pymysql.connect(host = settings['db_host'], 
                     user = settings['db_user'], 
                     passwd = settings['db_password'], 
                     db = settings['db_database'],
                     charset='utf8')
    cursor = db.cursor()
    if len(args) != 0:
      cursor.execute(sql, args)
    else:
      cursor.execute(sql)
    db.commit()
    db.close()
  except Exception as e:
    print(traceback.format_exc(e))


def get_customer(customer_name):
  # Given the {customer_id}, get the {customer_id, phone, address} of a customer.
  sql = 'select customer_id, phone, address from customer where customer_id = %s'
  data = query(sql, customer_name)[0]
  return {'customer_id': data[0], 'phone': data[1], 'address': data[2]}

def get_restaurant(restaurant_name):
  # Given the {restaurant_id} get the {restaurant_id, phone, food} of a restaurant.
  sql = 'select restaurant_id, phone, food from restaurant where restaurant_id = %s'
  data =  list(query(sql, restaurant_name)[0])
  return {'restaurant_id': data[0], 'phone': data[1], 'food': json.loads(data[2])}

def write_order(data, price):
  # Insert an order with (customer_id, restaurant_id, date, price, food)
  sql = 'insert into orders (customer_id, restaurant_id, date, price, food) values (%s, %s, %s, %s, %s)'
  insert_update(sql, data['customer_id'], data['restaurant_id'], data['date'], price, json.dumps(data['food']))

def count_price(restaurant_id, food_list):
  sql = 'select food from restaurant where restaurant_id = %s'
  food_price = json.loads(query(sql, restaurant_id)[0][0])
  price = 0
  for food in food_list:
    for each in food_price:
      if food['food_id'] == each['food_id']:
        price += each['price'] * food['num']
        break
  return price

  
if __name__ == '__main__':
  sql = 'insert into customer (customer_id, customer_name, phone, address, default_address) values (%s, %s, %s, %s, %s)'
  insert_update(sql, 'eatme', 'eatme', '1234567890', json.dumps([{"address_id":1,"place":"肾六楼下"}]), 1)

  sql = 'insert into restaurant (restaurant_id, restaurant_name, phone, food) values (%s, %s, %s, %s)'
  insert_update(sql, 'eatme_res', 'eatme_res', '1234567890', json.dumps([{"food_id": 1,"food_type": "staple","food_name": "麻辣香锅","price": 25.0,"num": 10,"image_url": "/img/1.png","detail": "1"}]))