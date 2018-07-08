import unittest
import requests
import pymysql
import json
from settings import settings
import traceback

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

class test_update_shopping_list(unittest.TestCase):

  def setUp(self):

    sql = 'INSERT INTO restaurant (restaurant_id, restaurant_name, phone, food, status, password) VALUES (%s, %s, %s, %s, %s, %s)'
    self.restaurant_id = 'test_res'
    self.restaurant_name = 'test_res'
    self.phone = '1234567890'
    self.res_food = [{"num": 10, "price": 25, "detail": "1", "food_id": 1, "food_name": "麻辣香锅", "food_type": "staple", "image_url": "/img/1.png"}, {"num": 10, "price": 13, "detail": "2", "food_id": 2, "food_name": "台湾卤肉饭", "food_type": "staple", "image_url": "/img/2.png"}]
    self.status = 0
    self.password = '13579'
    insert_update(sql, self.restaurant_id, self.restaurant_name, self.phone, json.dumps(self.res_food), self.status, self.password)

    sql = 'INSERT INTO customer (customer_id, customer_name, phone, address) VALUES (%s, %s, %s, %s)'
    self.customer_id = 'test_cust'
    self.customer_name = 'test_cust'
    self.phone = '1234567890'
    self.address = json.dumps([{"place": "shenliu", "address_id": 1}])
    insert_update(sql, self.customer_id, self.customer_name, self.phone, self.address)

    sql = 'INSERT INTO shopping_list (customer_id, restaurant_id, food, table_No) VALUES (%s, %s, %s, %s)'
    self.table_No = 1
    self.food = []
    insert_update(sql, self.customer_id, self.restaurant_id, json.dumps(self.food), self.table_No)


  def tearDown(self):
    
    sql = 'DELETE FROM shopping_list WHERE restaurant_id = %s'
    insert_update(sql, self.restaurant_id)
    sql = 'DELETE FROM customer WHERE customer_id = %s'
    insert_update(sql, self.customer_id)
    sql = 'DELETE FROM restaurant WHERE restaurant_id = %s'
    insert_update(sql, self.restaurant_id)

  def test_get(self):
    url = 'http://localhost:8887/shopping_list'

    new_sl = [
          {
              "food_id":1,
              "num":2
          },
          {
              "food_id":2,
              "num":1
          }
      ]

    msg = {
      "customer_id": self.customer_id,
      "restaurant_id": self.restaurant_id,
      "table_No": self.table_No,
      "shopping_list": new_sl
    }
    r = requests.post(url, json=msg)
    data = json.loads(r.text)['result']

    update_sl = [
          {
              "food_id":1,
              "num":2
          },
          {
              "food_id":2,
              "num":1
          }
      ]
    self.assertEqual(json.loads(data), update_sl)

if __name__ == '__main__':
  unittest.main()