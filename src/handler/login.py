import tornado, json, traceback, datetime
import mysql

class restaurant_login(tornado.web.RequestHandler):

  def initialize(self):
    self.res_status = {}

  def post(self):
    """
    Restaurant login. Given the id and password of a restaurant, check if they match.
    If match, response the restaurant's information,
     all shopping lists and all table orders of the restaurant.
    """
    try:
      data = json.loads(self.request.body)
      res = mysql.check_restaurant(data['restaurant_id'], data['password'])
      if res:
        self.res_status['state'] = 200
        self.res_status['result'] = mysql.get_restaurant(data['restaurant_id'])
        self.res_status['shoping_list'] = mysql.get_all_shopping_list(data['restaurant_id'])
        self.res_status['orders'] = mysql.get_all_table_order(data['restaurant_id'])
      else:
        self.res_status['state'] = 201

      self.write(json.dumps(self.res_status))
      self.finish()

    except Exception as e:
      self.res_status['state'] = 403
      self.res_status['detail'] = 'unknown error'
      self.write(json.dumps(self.res_status))
      self.set_status(403)
      self.finish()
      print(traceback.format_exc(e))