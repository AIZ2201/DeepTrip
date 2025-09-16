/*
 Navicat Premium Data Transfer

 Source Server         : localhost_3306
 Source Server Type    : MySQL
 Source Server Version : 80402 (8.4.2)
 Source Host           : localhost:3306
 Source Schema         : deeptrip

 Target Server Type    : MySQL
 Target Server Version : 80402 (8.4.2)
 File Encoding         : 65001

 Date: 16/09/2025 11:25:56
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for admin_login
-- ----------------------------
DROP TABLE IF EXISTS `admin_login`;
CREATE TABLE `admin_login`  (
  `admin_id` int NOT NULL AUTO_INCREMENT COMMENT '管理员主键',
  `username` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '登录账号',
  `password` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '密码',
  `email` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '邮箱',
  PRIMARY KEY (`admin_id`) USING BTREE,
  UNIQUE INDEX `uk_username`(`username` ASC) USING BTREE,
  UNIQUE INDEX `uk_email`(`email` ASC) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 2 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci COMMENT = '管理员登录表' ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of admin_login
-- ----------------------------
INSERT INTO `admin_login` VALUES (1, 'admin', '111', '111@admin.com');

-- ----------------------------
-- Table structure for feedback
-- ----------------------------
DROP TABLE IF EXISTS `feedback`;
CREATE TABLE `feedback`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `merchant_id` int NOT NULL,
  `service_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `overall_rating` int NOT NULL,
  `environment_rating` int NOT NULL,
  `service_rating` int NOT NULL,、、
  `value_rating` int NOT NULL,
  `feedback_content` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL,
  `images` json NULL,
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `merchant_feedback` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL,
  `merchant_reply_time` datetime NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `feedback_user_login_id_fk`(`user_id` ASC) USING BTREE,
  INDEX `feedback_merchant_id_fk`(`merchant_id` ASC) USING BTREE,
  CONSTRAINT `feedback_merchant_id_fk` FOREIGN KEY (`merchant_id`) REFERENCES `merchant_login` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `feedback_user_login_id_fk` FOREIGN KEY (`user_id`) REFERENCES `user_login` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of feedback
-- ----------------------------

-- ----------------------------
-- Table structure for merchant_login
-- ----------------------------
DROP TABLE IF EXISTS `merchant_login`;
CREATE TABLE `merchant_login`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `email` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `phone` varchar(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `password` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `business_type` enum('hotel','attraction','restaurant','other') CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `status` enum('pending','active','suspended') CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT 'pending',
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 3 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of merchant_login
-- ----------------------------
INSERT INTO `merchant_login` VALUES (1, '12', '111@111.com', '12345679801', '11111111', 'hotel', 'active', '2025-09-09 10:09:53');
INSERT INTO `merchant_login` VALUES (2, '1143', '113@111.com', '15345678901', '111', 'hotel', 'pending', '2025-09-15 14:45:07');

-- ----------------------------
-- Table structure for merchant_order
-- ----------------------------
DROP TABLE IF EXISTS `merchant_order`;
CREATE TABLE `merchant_order`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `order_id` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `merchant_id` int NOT NULL,
  `user_id` int NOT NULL,
  `product_name` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `amount` decimal(10, 2) NOT NULL,
  `status` enum('pending','confirmed','completed','cancelled') CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT 'pending',
  `order_time` datetime NOT NULL,
  `status_text` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `order_id`(`order_id` ASC) USING BTREE,
  INDEX `merchant_order_merchant_login_id_fk`(`merchant_id` ASC) USING BTREE,
  INDEX `merchant_order_user_login_id_fk`(`user_id` ASC) USING BTREE,
  CONSTRAINT `merchant_order_merchant_login_id_fk` FOREIGN KEY (`merchant_id`) REFERENCES `merchant_login` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `merchant_order_user_login_id_fk` FOREIGN KEY (`user_id`) REFERENCES `user_login` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of merchant_order
-- ----------------------------

-- ----------------------------
-- Table structure for merchant_register_codes
-- ----------------------------
DROP TABLE IF EXISTS `merchant_register_codes`;
CREATE TABLE `merchant_register_codes`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `email` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `code` varchar(6) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `purpose` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT 'register',
  `used` tinyint(1) NOT NULL DEFAULT 0,
  `expires_at` datetime NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 2 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of merchant_register_codes
-- ----------------------------
INSERT INTO `merchant_register_codes` VALUES (1, '111@111.com', '507610', 'register', 1, '2025-09-09 10:19:03', '2025-09-09 10:09:02');

-- ----------------------------
-- Table structure for orders
-- ----------------------------
DROP TABLE IF EXISTS `orders`;
CREATE TABLE `orders`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `merchant_id` int NOT NULL,
  `category` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `service_name` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `service_start_time` datetime NOT NULL,
  `service_end_time` datetime NOT NULL,
  `book_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `price` decimal(10, 2) NOT NULL,
  `phonenumber` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `customer_name` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `status` enum('pending','confirmed','completed','cancelled') CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT 'pending',
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `orders_user_id_fk`(`user_id` ASC) USING BTREE,
  INDEX `orders_merchant_id_fk`(`merchant_id` ASC) USING BTREE,
  CONSTRAINT `orders_merchant_id_fk` FOREIGN KEY (`merchant_id`) REFERENCES `merchant_login` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `orders_user_id_fk` FOREIGN KEY (`user_id`) REFERENCES `user_login` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of orders
-- ----------------------------

-- ----------------------------
-- Table structure for password_reset_codes
-- ----------------------------
DROP TABLE IF EXISTS `password_reset_codes`;
CREATE TABLE `password_reset_codes`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `email` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `code` varchar(6) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `expire_at` datetime NOT NULL,
  `used` tinyint(1) NOT NULL DEFAULT 0,
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of password_reset_codes
-- ----------------------------

-- ----------------------------
-- Table structure for shop_info
-- ----------------------------
DROP TABLE IF EXISTS `shop_info`;
CREATE TABLE `shop_info`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `merchant_id` int NOT NULL,
  `name` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `category` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `price_range` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `description` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `address` varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `city` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `district` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `phone` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `email` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `website` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `wechat` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `holiday_info` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL,
  `images` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL,
  `business_hours` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL,
  `service_items` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL,
  `created_at` datetime NULL DEFAULT CURRENT_TIMESTAMP,
  `status` enum('save_npush','save_push','formal','nsave') CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT 'nsave',
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `shop_info_merchant_login_id_fk`(`merchant_id` ASC) USING BTREE,
  CONSTRAINT `shop_info_merchant_login_id_fk` FOREIGN KEY (`merchant_id`) REFERENCES `merchant_login` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 6 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of shop_info
-- ----------------------------
INSERT INTO `shop_info` VALUES (1, 1, '九龙湖宾馆', 'hotel', 'standard', '坐落于东大九龙湖西北角，直通地铁5号线', '东大九龙湖', '南京', '秣陵街道', '114514', '', '', '', '', '[]', '[{\"day\": \"周一\", \"isOpen\": true, \"startTime\": \"09:00\", \"endTime\": \"18:00\"}, {\"day\": \"周二\", \"isOpen\": true, \"startTime\": \"09:00\", \"endTime\": \"18:00\"}, {\"day\": \"周三\", \"isOpen\": true, \"startTime\": \"09:00\", \"endTime\": \"18:00\"}, {\"day\": \"周四\", \"isOpen\": true, \"startTime\": \"09:00\", \"endTime\": \"18:00\"}, {\"day\": \"周五\", \"isOpen\": true, \"startTime\": \"09:00\", \"endTime\": \"18:00\"}, {\"day\": \"周六\", \"isOpen\": false, \"startTime\": \"09:00\", \"endTime\": \"18:00\"}, {\"day\": \"周日\", \"isOpen\": false, \"startTime\": \"09:00\", \"endTime\": \"18:00\"}]', '[{\"name\":\"豪华大床房\",\"price\":\"300\"}]', '2025-09-12 15:24:21', 'save_push');
INSERT INTO `shop_info` VALUES (2, 1, '榴园宾馆', 'hotel', 'standard', '坐拥四牌楼市中心美景，体验东大的蒋匪遗风', '四牌楼2号', '南京', '四牌楼', '114514', '', '', '', '', '[]', '[{\"day\": \"周一\", \"isOpen\": true, \"startTime\": \"09:00\", \"endTime\": \"18:00\"}, {\"day\": \"周二\", \"isOpen\": true, \"startTime\": \"09:00\", \"endTime\": \"18:00\"}, {\"day\": \"周三\", \"isOpen\": true, \"startTime\": \"09:00\", \"endTime\": \"18:00\"}, {\"day\": \"周四\", \"isOpen\": true, \"startTime\": \"09:00\", \"endTime\": \"18:00\"}, {\"day\": \"周五\", \"isOpen\": true, \"startTime\": \"09:00\", \"endTime\": \"18:00\"}, {\"day\": \"周六\", \"isOpen\": false, \"startTime\": \"09:00\", \"endTime\": \"18:00\"}, {\"day\": \"周日\", \"isOpen\": false, \"startTime\": \"09:00\", \"endTime\": \"18:00\"}]', '[{\"name\":\"豪华三床亲子房\",\"price\":\"500\"}]', '2025-09-13 10:35:21', 'save_push');
INSERT INTO `shop_info` VALUES (3, 1, '绝云间民宿', 'hotel', 'standard', '象鼻山旁山水烟云，你将感受仙境', '象山路', '桂林', '象山', '114514', '', '', '', '', '[]', '[{\"day\": \"周一\", \"isOpen\": true, \"startTime\": \"09:00\", \"endTime\": \"18:00\"}, {\"day\": \"周二\", \"isOpen\": true, \"startTime\": \"09:00\", \"endTime\": \"18:00\"}, {\"day\": \"周三\", \"isOpen\": true, \"startTime\": \"09:00\", \"endTime\": \"18:00\"}, {\"day\": \"周四\", \"isOpen\": true, \"startTime\": \"09:00\", \"endTime\": \"18:00\"}, {\"day\": \"周五\", \"isOpen\": true, \"startTime\": \"09:00\", \"endTime\": \"18:00\"}, {\"day\": \"周六\", \"isOpen\": false, \"startTime\": \"09:00\", \"endTime\": \"18:00\"}, {\"day\": \"周日\", \"isOpen\": false, \"startTime\": \"09:00\", \"endTime\": \"18:00\"}]', '[{\"name\":\"全景山水大床房\",\"price\":\"600\"}]', '2025-09-13 11:02:53', 'save_push');
INSERT INTO `shop_info` VALUES (4, 1, '快樂食间', 'restaurant', 'standard', '梅园的，东大的，南京的，中国的，世界的快乐时间！', '梅园商务区', '南京', '梅园', '114514', '', '', '', '', '[]', '[{\"day\": \"周一\", \"isOpen\": true, \"startTime\": \"09:00\", \"endTime\": \"18:00\"}, {\"day\": \"周二\", \"isOpen\": true, \"startTime\": \"09:00\", \"endTime\": \"18:00\"}, {\"day\": \"周三\", \"isOpen\": true, \"startTime\": \"09:00\", \"endTime\": \"18:00\"}, {\"day\": \"周四\", \"isOpen\": true, \"startTime\": \"09:00\", \"endTime\": \"18:00\"}, {\"day\": \"周五\", \"isOpen\": true, \"startTime\": \"09:00\", \"endTime\": \"18:00\"}, {\"day\": \"周六\", \"isOpen\": false, \"startTime\": \"09:00\", \"endTime\": \"18:00\"}, {\"day\": \"周日\", \"isOpen\": false, \"startTime\": \"09:00\", \"endTime\": \"18:00\"}]', '[{\"name\":\"平价大伙\",\"price\":\"10\"}]', '2025-09-15 15:34:10', 'formal');
INSERT INTO `shop_info` VALUES (5, 1, '玄武湖公园', 'attraction', 'standard', '南京市中心的皇家园林，古城墙围绕，有多少文人墨客的足迹...', '鸡鸣寺旁', '南京', '玄武湖', '114514', '', '', '', '', '[]', '[{\"day\": \"周一\", \"isOpen\": true, \"startTime\": \"09:00\", \"endTime\": \"18:00\"}, {\"day\": \"周二\", \"isOpen\": true, \"startTime\": \"09:00\", \"endTime\": \"18:00\"}, {\"day\": \"周三\", \"isOpen\": true, \"startTime\": \"09:00\", \"endTime\": \"18:00\"}, {\"day\": \"周四\", \"isOpen\": true, \"startTime\": \"09:00\", \"endTime\": \"18:00\"}, {\"day\": \"周五\", \"isOpen\": true, \"startTime\": \"09:00\", \"endTime\": \"18:00\"}, {\"day\": \"周六\", \"isOpen\": false, \"startTime\": \"09:00\", \"endTime\": \"18:00\"}, {\"day\": \"周日\", \"isOpen\": false, \"startTime\": \"09:00\", \"endTime\": \"18:00\"}]', '[{\"name\":\"玄武湖公园\",\"price\":\"0\"}]', '2025-09-15 15:34:10', 'formal');

-- ----------------------------
-- Table structure for user_login
-- ----------------------------
DROP TABLE IF EXISTS `user_login`;
CREATE TABLE `user_login`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `password` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `email` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `phonenumber` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 3 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of user_login
-- ----------------------------
INSERT INTO `user_login` VALUES (1, '11', 'a1111111', '112@111.com', '18172645645');
INSERT INTO `user_login` VALUES (2, '434', '11111111', '123@111.com', '18172641645');

SET FOREIGN_KEY_CHECKS = 1;
