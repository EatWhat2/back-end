import unittest
import requests
import pymysql
import json
from settings import settings

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

class test_table_order(unittest.TestCase):

  def setUp(self):
    sql = 'INSERT INTO restaurant (restaurant_id, restaurant_name, phone, food, status, password) VALUES (%s, %s, %s, %s, %s, %s)'
    self.restaurant_id = 'test_res'
    self.restaurant_name = 'test_res'
    self.phone = '1234567890'
    self.food = [{"num": 10, "price": 25, "detail": "1", "food_id": 1, "food_name": "麻辣香锅", "food_type": "staple", "image_url": "/img/1.png"}, {"num": 10, "price": 13, "detail": "2", "food_id": 2, "food_name": "台湾卤肉饭", "food_type": "staple", "image_url": "/img/2.png"}]
    self.status = 0
    self.password = '13579'
    insert_update(sql, self.restaurant_id, self.restaurant_name, self.phone, json.dumps(self.food), self.status, self.password)

    sql = 'INSERT INTO customer (customer_id, customer_name, phone, address) VALUES (%s, %s, %s, %s)'
    self.customer_id = 'test_cust'
    self.customer_name = 'test_cust'
    self.phone = '1234567890'
    self.address = json.dumps([{"place": "shenliu", "address_id": 1}])
    insert_update(sql, self.customer_id, self.customer_name, self.phone, self.address)

  def tearDown(self):
    sql = 'DELETE FROM shopping_list WHERE restaurant_id = %s'
    insert_update(sql, self.restaurant_id)
    sql = 'DELETE FROM restaurant WHERE restaurant_id = %s'
    insert_update(sql, self.restaurant_id)
    sql = 'DELETE FROM customer WHERE customer_id = %s'
    insert_update(sql, self.customer_id)

  def test_get(self):
    url = 'http://localhost:8887/table_order?customer_id={}&restaurant_id={}&table_No={}'.format(self.customer_id, self.restaurant_id, 1)
    r = requests.get(url)
    data = json.loads(r.text)['result']
    self.assertEqual(data['restaurant_id'], self.restaurant_id)
    self.assertEqual(data['phone'], self.phone)
    self.assertEqual(data['food'], self.food)
    self.assertEqual(data['private_shopping_list'], [])
    self.assertEqual(data['public_shopping_list'], [])

if __name__ == '__main__':
  unittest.main()