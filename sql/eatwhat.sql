CREATE TABLE IF NOT EXISTS `customer` (
  `customer_id` varchar(10) not null,
  `customer_name` varchar(32) not null,
  `phone` varchar(16) not null,
  `address` json,
  `default_address` int unsigned DEFAULT 0,
  PRIMARY KEY(`customer_id`)
) ENGINE = InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE IF NOT EXISTS `restaurant` (
  `restaurant_id` varchar(10) not null,
  `restaurant_name` varchar(32) not null,
  `phone` varchar(16) not null,
  `food` json,
  `password` varchar(32) not null,
  `status` tinyint(1) not null,
  PRIMARY KEY(`restaurant_id`)
) ENGINE = InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE IF NOT EXISTS `orders` (
  `order_id` int unsigned not null auto_increment,
  `customer_id` varchar(10) not null,
  `restaurant_id` varchar(10) not null,
  `date` varchar(32) not null,
  `price` int unsigned not null, 
  `food` json,
  `comment` json,
  PRIMARY KEY(`order_id`),
  FOREIGN KEY (`customer_id`) REFERENCES customer(`customer_id`),
  FOREIGN KEY (`restaurant_id`) REFERENCES restaurant(`restaurant_id`)
) ENGINE = InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE IF NOT EXISTS `table_orders` (
  `order_id` int unsigned not null auto_increment,
  `customer_id` varchar(10) not null,
  `restaurant_id` varchar(10) not null,
  `date` varchar(32) not null,
  `price` int unsigned not null, 
  `food` json,
  `table_No` int unsigned not null,
  `comment` json,
  PRIMARY KEY(`order_id`),
  FOREIGN KEY (`customer_id`) REFERENCES customer(`customer_id`),
  FOREIGN KEY (`restaurant_id`) REFERENCES restaurant(`restaurant_id`)
) ENGINE = InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE IF NOT EXISTS `shopping_list` (
  `shopping_list_id` int unsigned not null auto_increment,
  `table_No` int unsigned not null,
  `restaurant_id` varchar(32) not null,
  `customer_id` varchar(32) not null,
  `food` json,
  PRIMARY KEY(`shopping_list_id`),
  FOREIGN KEY (`restaurant_id`) REFERENCES restaurant(`restaurant_id`)
) ENGINE = InnoDB DEFAULT CHARSET=utf8;