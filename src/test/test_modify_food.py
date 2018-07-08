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

class test_modify_food(unittest.TestCase):

  def setUp(self):
    sql = 'INSERT INTO restaurant (restaurant_id, restaurant_name, phone, food, status, password) VALUES (%s, %s, %s, %s, %s, %s)'
    self.restaurant_id = 'test_res'
    self.restaurant_name = 'test_res'
    self.phone = '1234567890'
    self.food = []
    self.status = 0
    self.password = '13579'
    insert_update(sql, self.restaurant_id, self.restaurant_name, self.phone, json.dumps(self.food), self.status, self.password)

  def tearDown(self):
    sql = 'DELETE FROM restaurant WHERE restaurant_id = %s'
    insert_update(sql, self.restaurant_id)

  def test_get(self):
    url = 'http://localhost:8887/restaurant_food'

    food = [
            {
                "food_id": 1,
                "food_type": "staple",
                "food_name": "malaxiangguo",
                "price": 25.0,
                "num": 10,
                "image_url": "/img/1.png",
                "detail": "1"
            },
            {
                "food_id": 2,
                "food_type": "staple",
                "food_name": "luroufan",
                "price": 13.0,
                "num": 10,
                "image_url": "/img/2.png",
                "detail": "2"
            },
            {
                "food_id": 3,
                "food_type": "snack",
                "food_name": "shutiao",
                "price": 8.0,
                "num": 10,
                "image_url": "/img/3.png",
                "detail": "3"
            },
            {
                "food_id": 4,
                "food_type": "snack",
                "food_name": "jichi",
                "price": 10.0,
                "num": 10,
                "image_url": "/img/4.png",
                "detail": "4"
            }
        ]
    msg = {
    "restaurant_id": self.restaurant_id,
    "food": food
    }
    r = requests.post(url, json=msg)
    
    sql = 'SELECT food FROM restaurant WHERE restaurant_id = %s'
    rst = json.loads(query(sql, self.restaurant_id)[0][0])

    self.assertEqual(rst, food)

if __name__ == '__main__':
  unittest.main()