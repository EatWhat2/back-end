import tornado, json, traceback, datetime
import mysql

class restaurant_status(tornado.web.RequestHandler):

  def initialize(self):
    self.res_status = {}

  def post(self):
    # Update the status of a restaurant.
    # {data['status']}:
    #   1 if the restaurant is working.
    #   0 if the restaurant is resting.
    try:
      data = json.loads(self.request.body)
      mysql.set_restaurant_status(data['restaurant_id'], data['status'])
      
      self.res_status['state'] = 200
      self.write(json.dumps(self.res_status))
      self.finish()

    except Exception as e:
      self.res_status['state'] = 403
      self.res_status['detail'] = 'unknown error'
      self.write(json.dumps(self.res_status))
      self.set_status(403)
      self.finish()
      print(traceback.format_exc(e))

class modify_food(tornado.web.RequestHandler):

  def initialize(self):
    self.res_status = {}

  def post(self):
    # Update the food list of a restaurant, given the restaurant's id.
    try:
      data = json.loads(self.request.body)
      mysql.write_food(data['restaurant_id'], data['food'])
      
      self.res_status['state'] = 200
      self.write(json.dumps(self.res_status))
      self.finish()

    except Exception as e:
      self.res_status['state'] = 403
      self.res_status['detail'] = 'unknown error'
      self.write(json.dumps(self.res_status))
      self.set_status(403)
      self.finish()
      print(traceback.format_exc(e))

class order_refresh(tornado.web.RequestHandler):

  def initialize(self):
    self.res_status = {}

  def get(self):
    # Update all table orders of a restaurant.
    try:
      restaurant_id = self.get_argument("restaurant_id")
      data = mysql.get_all_table_order(restaurant_id)
      self.res_status['orders'] = data
      self.write(json.dumps(self.res_status))
      self.finish()

    except Exception as e:
      self.res_status['result'] = 'error'
      self.write(json.dumps(self.res_status))
      self.set_status(403)
      self.finish()
      print(traceback.format_exc(e))
