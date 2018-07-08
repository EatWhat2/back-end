# !/usr/bin/env python3

import tornado, json, traceback, datetime
import mysql

class order(tornado.web.RequestHandler):

  def initialize(self):
    self.res_status = {}

  def post(self):
    try:
      print(self.request.body)
      data = json.loads(self.request.body)
      print(data)
      if mysql.get_restaurant_status(data['restaurant_id']):
        if mysql.check_order(data['restaurant_id'], data['food']):
          # Count order price.
          price = mysql.count_price(data['restaurant_id'], data['food'])
          self.res_status['state'] = 200
          self.res_status['detail'] = '下单成功'
          mysql.write_order(data, price)
          print(price)
        else:
          # The order is invalid.
          self.res_status['state'] = 201
          self.res_status['detail'] = '食物缺失'
      else:
        # The resturant is resting.
        self.res_status['state'] = 202
        self.res_status['detail'] = '商家打烊'

      self.write(json.dumps(self.res_status))
      self.finish()

    except Exception as e:
      self.res_status['state'] = 403
      self.res_status['detail'] = 'unknown error'
      self.write(json.dumps(self.res_status))
      self.set_status(403)
      self.finish()
      print(traceback.format_exc(e))