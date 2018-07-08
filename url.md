# 1. 顾客信息获取

## 1.1 基本信息

接口名称：顾客信息获取

接口地址："http://localhost:8888"

请求方法：GET

请求数据类型：X-WWW-FORM-URLENCODED

响应类型：JSON

状态：有效

接口描述：

​ 使用微信名获取顾客信息



## 1.2 请求参数

| 参数名称      | 是否必须 | 数据类型 | 默认值 | 描述       |
| ------------- | -------- | -------- | ------ | ---------- |
| customer_name | true     | string   | None   | 用户微信名 |



## 1.3 响应参数

| 参数名称    | 是否必须 | 数据类型      | 描述                         |
| ----------- | -------- | ------------- | ---------------------------- |
| result      | true     | object        | 返回结果                     |
| customer_id | true     | string        | 顾客ID，用于索引顾客         |
| phone       | true     | string        | 顾客电话                     |
| address     | true     | array[object] | 顾客地址，多个地址用数组表示 |
| address_id  | true     | number        | 地址ID                       |
| place       | true     | string        | 具体地址                     |



## 1.4 示例数据

请求："http://localhost:8888/customer_name=123"

响应：

```JSON
{
    "result":{
        "customer_id": 1,
        "phone":10000,
        "address":[
            {
                "address_id":1,
                "place":"肾六楼下"
            },
            {
                "address_id":2,
                "place":"公教楼"
            }]
    }
}
```



# 2. 商家信息获取

## 2.1 基本信息

接口名称：商家信息获取

接口地址："http://localhost:8888/"

请求方法：GET

请求数据类型：X-WWW-FORM-URLENCODED

响应类型：JSON

状态：有效

接口描述：

​ 使用商家名称获取商家信息



## 2.2 请求参数

| 参数名称        | 是否必须 | 数据类型 | 默认值 | 描述     |
| --------------- | -------- | -------- | ------ | -------- |
| restaurant_name | true     | string   | None   | 商家名称 |



## 2.3 响应参数

| 参数名称      | 是否必须 | 数据类型      | 描述                   |
| ------------- | -------- | ------------- | ---------------------- |
| result        | true     | object        | 返回结果               |
| restaurant_id | true     | string        | 商家ID，用于索引商家   |
| phone         | true     | string        | 商家电话               |
| food          | true     | array[object] | 食品，用于索引食品     |
| food_id       | true     | number        | 食品ID，用于索引食品   |
| food_type     | true     | string        | 食品类型，用于分类食品 |
| food_name     | true     | string        | 食品名称               |
| price         | true     | number        | 食品价格               |
| num           | true     | number        | 食品剩余数量           |
| image_url     | true     | string        | 食品图片URL            |
| detail        | true     | string        | 食品描述               |



## 2.4 示例数据

请求："http://localhost:8888/restaurant_name=123"
返回：

```json
{
    "result": {
        "restaurant_id": 1,
        "phone": 10000,
        "food": [
            {
                "food_id": 1,
                "food_type": "staple",
                "food_name": "麻辣香锅",
                "price": 25.0,
                "num": 10,
                "image_url": "/img/1.png",
                "detail": "1"
            },
            {
                "food_id": 2,
                "food_type": "staple",
                "food_name": "台湾卤肉饭",
                "price": 13.0,
                "num": 10,
                "image_url": "/img/2.png",
                "detail": "2"
            },
            {
                "food_id": 3,
                "food_type": "snack",
                "food_name": "薯条",
                "price": 8.0,
                "num": 10,
                "image_url": "/img/3.png",
                "detail": "3"
            },
            {
                "food_id": 4,
                "food_type": "snack",
                "food_name": "鸡翅",
                "price": 10.0,
                "num": 10,
                "image_url": "/img/4.png",
                "detail": "4"
            }
        ]
    }
}
```



# 3. 订单提交

## 3.1 基本信息

接口名称：订单提交

接口地址："http://localhost:8888/"

请求方法：POST

请求数据类型：JSON

响应类型：JSON

状态：有效

接口描述:

​ 顾客提交订单信息



## 3.2 请求参数

| 参数名称      | 是否必须 | 数据类型      | 默认值 | 描述                 |
| ------------- | -------- | ------------- | ------ | -------------------- |
| customer_id   | true     | number        | 0      | 顾客ID，用于索引顾客 |
| restaurant_id | true     | number        | 0      | 商家ID，用于索引商家 |
| date          | true     | string        | ""     | 订单时间             |
| price         | true     | number        | 0      | 订单总价             |
| food          | true     | array[object] | None   | 订单食品             |
| food_id       | true     | number        |        | 食品ID，用于索引食品 |
| num           | true     | number        |        | 食品数量             |



## 3.3 响应参数

| 参数名称 | 是否必须 | 数据类型 | 描述         |
| -------- | -------- | -------- | ------------ |
| state    | true     | number   | 订单状态码   |
| detail   | true     | string   | 订单状态详情 |



## 3.4 示例数据

订单状态码：
  200 — 下单成功
  201 — 食品缺失
  202 — 商家打烊

请求：
  url: "http://localhost:8888/"

​ data:

```json
{
    "customer_id": 1,
    "restaurant_id": 1,
    "date": "2018-01-01 13:59:59",
    "price": 35.5,
    "food": [
        {
            "food_id": 1,
            "num": 2
        },
        {
            "food_id": 2,
            "num": 1
        }
    ]
}
```



响应：

```json
{
    "state": 200,
    "detail": "下单成功"
}
```
