# !/usr/bin/env python3
# -*- coding: utf-8 -*- 

import pymysql, traceback, datetime, json
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


def get_customer(customer_id):
  # Given the {customer_id}, get the {customer_id, phone, address} of a customer.
  sql = 'select customer_id, phone, address from customer where customer_id = %s'
  data = query(sql, customer_id)[0]
  return {'customer_id': data[0], 'phone': data[1], 'address': data[2]}

def get_restaurant(restaurant_id):
  # Given the {restaurant_id} get the {restaurant_id, phone, food} of a restaurant.
  sql = 'select restaurant_id, restaurant_name, phone, food from restaurant where restaurant_id = %s'
  data =  list(query(sql, restaurant_id)[0])
  return {'restaurant_id': data[0], 'restaurant_name': data[1], 'phone': data[2], 'food': json.loads(data[3])}

def write_order(data, price):
  # Insert an order.
  # [Not used]
  sql = 'insert into orders (customer_id, restaurant_id, date, price, food) values (%s, %s, %s, %s, %s)'
  insert_update(sql, data['customer_id'], data['restaurant_id'], data['date'], price, json.dumps(data['food']))

def write_table_order(data):
  # Insert an table order made by a customer.
  sql = 'insert into table_orders (customer_id, restaurant_id, date, price, food, table_No) values (%s, %s, %s, %s, %s, %s)'
  insert_update(sql, data['customer_id'], data['restaurant_id'], data['date'], data['price'], json.dumps(data['food']), data['table_No'])

def get_all_table_order(restaurant_id):
  # Return all table orders of a restaurant.
  # The orders can be made by different customers of different tables.
  sql = 'SELECT date, table_No, price, food FROM table_orders WHERE restaurant_id = %s'
  data = list(query(sql, restaurant_id))

  rtn = []

  for i in range(len(data)):
    rtn.append({'date': data[i][0], 'table_No': data[i][1], 'price': data[i][2], 'food': json.loads(data[i][3])})

  return rtn

def count_price(restaurant_id, food_list):
  # Count the total price of the food list.
  # [Not used]
  sql = 'select food from restaurant where restaurant_id = %s'
  food_price = json.loads(query(sql, restaurant_id)[0][0])
  price = 0

  # Iter all food in order. If a food is availuable in restuarant, add to the total price.
  for food in food_list:
    for each in food_price:
      if food['food_id'] == each['food_id']:
        price += each['price'] * food['num']
        break
  return price

def get_shopping_list(table_No, restaurant_id, customer_id):
  # Get all food in a customer's shopping list at a table.
  # If the list doesn't exist, create one.
  sql = 'select food from shopping_list where table_No = %s and restaurant_id = %s and customer_id = %s'
  data = list(query(sql, table_No, restaurant_id, customer_id))

  if len(data) == 0:   # haven't created this shopping_list
    sql = 'insert into shopping_list (table_No, restaurant_id, customer_id) values (%s, %s, %s)'
    insert_update(sql, table_No, restaurant_id, customer_id)
    return None

  return data[0][0]

def write_customer_shopping_list(food, table_No, restaurant_id, customer_id):
  # Write the shopping list made by a customer of a table.
  # If the list exist in the database, update it.
  # Otherwise, create one in the database.

  # Check if customer have created this shopping_list before.
  sql = 'select food from shopping_list where table_No = %s and restaurant_id = %s and customer_id = %s'
  data = list(query(sql, table_No, restaurant_id, customer_id))

  if len(data) == 0:  # Haven't created this shopping_list. create one.
    sql = 'insert into shopping_list (table_No, restaurant_id, customer_id, food) values (%s, %s, %s, %s)'
    insert_update(sql, table_No, restaurant_id, customer_id, json.dumps(food))
  else:  # Update customer's shopping_list.
    sql = 'update shopping_list set food = %s where table_No = %s and restaurant_id = %s and customer_id = %s'
    insert_update(sql, json.dumps(food), table_No, restaurant_id, customer_id)

def get_table_shopping_list(table_No, restaurant_id):
  # Get all food ordered by a table.
  sql = 'select food from shopping_list where table_No = %s and restaurant_id = %s'
  data = list(query(sql, table_No, restaurant_id))

  return data

def get_all_shopping_list(restaurant_id):
  # Get all food ordered in a restaurant.
  sql = 'select food from shopping_list where restaurant_id = %s'
  data = list(query(sql, restaurant_id))

  data = [json.loads(x[0]) for x in data if x[0]]
  data = [x for x in data if len(x) > 0]

  return data

def write_shopping_list(restaurant_id, table_No, shopping_list):
  sql = 'UPDATE shopping_list SET food = %s WHERE restaurant_id = %s and table_No = %s'
  insert_update(sql, json.dumps(shopping_list), restaurant_id, table_No)
  
def check_restaurant(restaurant_id, password):
  """
    Check if the restaurant id matches the password.
    Return:
      True if they match.
      False if password is wrong or id doesn't exist.
  """
  sql = 'select * from restaurant where restaurant_id = %s and password = %s'
  data = list(query(sql, restaurant_id, password))
  if len(data) == 0:   # username or password wrong
    return 0
  else:
    return 1

def check_order(restaurant_id, food_list):
  """
    Check if the order is valid, that is all food in order are available in the restaurant.
    May be time consuming, because the code check the foods iterally.
    Return: 
      True if order valid
      False if order invalid.
  """
  sql = 'select food from restaurant where restaurant_id = %s'
  food_price = json.loads(query(sql, restaurant_id)[0][0])
  price = 0

  for order_food in food_list:
    is_food_available = False

    for restaurant_food in food_price:
      if order_food['food_id'] == restaurant_food['food_id']:
        is_food_available = True
        break

    # The food is invalid, so the order is invalid.
    if not is_food_available:
      return False
  return True

def set_restaurant_status(restaurant_id, status):
  """
  Update a restaurant's status.
  :param restaurant_id: The id of a restaurant.
  :param status: 1 if the restaurant is working, 0 if resting.
  """
  sql = 'UPDATE restaurant SET status = %s WHERE restaurant_id = %s'
  insert_update(sql, status, restaurant_id)

def get_restaurant_status(restaurant_id):
  """
  Get a restaurant's status(working or resting).
  :param restaurant_id: The id of a restaurant.
  :return: 1 if the restaurant is working, 0 if resting.
  """
  sql = 'select status from restaurant where restaurant_id = %s'
  return query(sql, restaurant_id)[0][0]

def write_food(restaurant_id, food):
  # Update the food list of a restaurant.
  sql = 'UPDATE restaurant SET food = %s WHERE restaurant_id = %s'
  insert_update(sql, json.dumps(food), restaurant_id)


if __name__ == '__main__':
  food = [{'food_id':1,'num':2},{'food_id':2,'num':1}]
  print(count_price('zyf', food))