# database table design ver0.1

---
## customer
|字段|类型|说明|
|:--:|:--:|:--:|
|customer_id|varchar(10) not null|主键，用餐者id|
|customer_name|varchar(32) not null|用户名。通常就是微信号|
|phone|varchar(16) not null|电话|
|address|json|送餐地址。ex.[{'address_id':1,'place':'肾六楼下'},{'address_id':1,'place':'公教楼'}]|
|default_address|int unsigned|default address id|

**注：看需求要不要加点额外信息。比如红包啥的**

## restaurant
|字段|类型|说明|
|:--:|:--:|:--:|
|restaurant_id|varchar(10) not null|主键，商家id|
|restaurant_name|varchar(32) not null|用户名。不必是微信号|
|phone|varchar(16) not null|telephone|
|food|json|出售中食物。ex. [{'food_id':1, 'food_type':'staple', 'food_name': '麻辣香锅', 'food_price': 25.0, 'num':10, 'image_url': '/img/1.png', 'detail': '1'}, {'food_id':2, 'food_name': '台湾卤肉饭', 'food_price': 13.0, 'num':10, 'image_url': '/img/2.png', 'detail': '2'}]|

**注：商家的注册信息，营业执照等信息不放在数据库里**

## order
|字段|类型|说明|
|:--:|:--:|:--:|
|order_id|int unsigned not null auto_increment|主键，订单id|
|customer_id|varchar(10) not null|外键，用餐者id|
|restaurant_id|varchar(10) not null|外键，商家id|
|date|varchar(32) not null|下单时间|
|price|int unsigned|订单金额. count by back-end|
|food|json|具体食物。ex.[{'food_id':1, 'num':1},{'food_id':3, 'num':1}]|
|comment|json|用户评价。ex.{'star':5, 'text': '我永远喜欢冬阴功', 'hide_name':True}|

## shopping_list
|字段|类型|说明|
|:--:|:--:|:--:|
|shopping_list_id|int unsigned not null auto_increment|主键，购物车id|
|table_No|int unsigned not null|餐桌号|
|restaurant_id|varchar(10) not null|外键，商家id|
|food|json|具体食物。ex.[{'food_id':1, 'num':1},{'food_id':3, 'num':1}]|



by two2er.
