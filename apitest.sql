# Host: localhost  (Version: 5.7.26)
# Date: 2020-07-18 18:46:26
# Generator: MySQL-Front 5.3  (Build 4.234)

/*!40101 SET NAMES utf8 */;


#
# Structure for table "stock"
#

DROP TABLE IF EXISTS `stock`;
CREATE TABLE `stock` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL DEFAULT '' COMMENT '名称',
  `price` float(4,2) NOT NULL DEFAULT '0.00' COMMENT '价格',
  `count` int(11) NOT NULL COMMENT '库存',
  `sale` int(11) NOT NULL COMMENT '已售',
  `version` int(11) NOT NULL COMMENT '乐观锁，版本号',
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=22 DEFAULT CHARSET=utf8mb4;

#
# Data for table "stock"
#

/*!40000 ALTER TABLE `stock` DISABLE KEYS */;
INSERT INTO `stock` VALUES (11,'Book',12.50,0,0,1),(12,'Book',12.50,0,0,1),(13,'Book',12.50,100,0,1),(14,'Book',12.50,100,0,1),(15,'Book',16.50,100,0,1),(16,'Book',16.50,100,0,1),(17,'Book',16.50,100,0,1),(18,'Book',16.50,100,0,1),(19,'Book',16.50,100,0,1),(20,'Book',16.50,100,0,1),(21,'Book',16.50,100,0,1);
/*!40000 ALTER TABLE `stock` ENABLE KEYS */;

#
# Structure for table "stock_order"
#

DROP TABLE IF EXISTS `stock_order`;
CREATE TABLE `stock_order` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `sid` int(11) NOT NULL COMMENT '库存ID',
  `orderprice` float(4,2) NOT NULL DEFAULT '0.00' COMMENT '订单价格',
  `username` varchar(30) NOT NULL DEFAULT '' COMMENT '商品名称',
  `receiver` varchar(255) DEFAULT NULL,
  `phone` varchar(255) DEFAULT NULL,
  `address` varchar(255) DEFAULT NULL,
  `create_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '创建时间',
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=145 DEFAULT CHARSET=utf8mb4;

#
# Data for table "stock_order"
#

/*!40000 ALTER TABLE `stock_order` DISABLE KEYS */;
/*!40000 ALTER TABLE `stock_order` ENABLE KEYS */;

#
# Structure for table "userinfo"
#

DROP TABLE IF EXISTS `userinfo`;
CREATE TABLE `userinfo` (
  `Id` int(11) NOT NULL AUTO_INCREMENT,
  `IDCard` varchar(18) NOT NULL DEFAULT '',
  `Phone` varchar(15) NOT NULL DEFAULT '',
  `Address` varchar(255) NOT NULL DEFAULT '',
  PRIMARY KEY (`Id`)
) ENGINE=MyISAM AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4;

#
# Data for table "userinfo"
#

/*!40000 ALTER TABLE `userinfo` DISABLE KEYS */;
INSERT INTO `userinfo` VALUES (1,'970827198804175919','13800138000','北京市海淀区北四环西路888号'),(2,'720621199406056677','13800138001','福建省厦门市思明区西山街道999号'),(3,'84152519840225088X','13800138002','江苏省苏州市昆山市黄浦江路898号'),(4,'640403199008017641','13800138003','上海市浦东新区华夏路666号');
/*!40000 ALTER TABLE `userinfo` ENABLE KEYS */;

#
# Structure for table "users"
#

DROP TABLE IF EXISTS `users`;
CREATE TABLE `users` (
  `Id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL DEFAULT '',
  `password` varchar(255) NOT NULL DEFAULT '',
  PRIMARY KEY (`Id`)
) ENGINE=MyISAM AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 ROW_FORMAT=DYNAMIC;

#
# Data for table "users"
#

/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (1,'admin','5690dddfa28ae085d23518a035707282'),(2,'Mr.null','dc483e80a7a0bd9ef71d8cf973673924'),(3,'ZhangSan','5690dddfa28ae085d23518a035707282'),(4,'Lisi','dc483e80a7a0bd9ef71d8cf973673924');
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
