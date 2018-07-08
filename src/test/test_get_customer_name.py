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

class test_get_customer_name(unittest.TestCase):

  def setUp(self):
    sql = 'INSERT INTO customer (customer_id, customer_name, phone, address) VALUES (%s, %s, %s, %s)'
    self.customer_id = 'test_cust'
    self.customer_name = 'test_cust'
    self.phone = '1234567890'
    self.address = json.dumps([{"place": "shenliu", "address_id": 1}])
    insert_update(sql, self.customer_id, self.customer_name, self.phone, self.address)

  def tearDown(self):
    sql = 'DELETE FROM customer WHERE customer_id = %s'
    insert_update(sql, self.customer_id)

  def test_get(self):
    url = 'http://localhost:8887/customer_name={}'.format(self.customer_id)
    r = requests.get(url)
    data = json.loads(r.text)['result']
    self.assertEqual(data['customer_id'], self.customer_id)
    self.assertEqual(data['phone'], self.phone)
    self.assertEqual(data['address'], self.address)

if __name__ == '__main__':
  unittest.main()