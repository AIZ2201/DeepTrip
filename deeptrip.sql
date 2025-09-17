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

 Date: 17/09/2025 19:52:02
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
  `service_rating` int NOT NULL,
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
-- Table structure for main_route
-- ----------------------------
DROP TABLE IF EXISTS `main_route`;
CREATE TABLE `main_route`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `start` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `end` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `days` int NOT NULL,
  `budget` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `tags` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `description` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `main_route_user_login_id_fk`(`user_id` ASC) USING BTREE,
  CONSTRAINT `main_route_user_login_id_fk` FOREIGN KEY (`user_id`) REFERENCES `user_login` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 11 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of main_route
-- ----------------------------
INSERT INTO `main_route` VALUES (7, 1, '南京', '无锡', 4, '2000元', '未明确', '根据您从南京出发至无锡的自驾需求，结合途经城市特色景点及预算控制，为您定制以下5日深度游方案：\n\n**行程整体概述**\n自驾路线贯穿宁镇常锡四城精华景点，融合自然风光与人文景观，全程预算严格控制在2000元内。精选【栖霞山秋色】【镇江三山文化】【常州恐龙主题】【太湖绝佳处】四大核心体验，住宿优选高评分性价比酒店。\n\n---\n\n**每日详细行程**\n\n**DAY1（10.1）南京→镇江**\n🚗交通：南京市区→栖霞山（30分钟）→镇江金山景区（1小时）\n📍景点：\n1. 【栖霞山】（2.5小时）秋日红叶胜地，登千佛岩俯瞰长江，红枫与古刹相映成趣\n2. 【金山寺】（2小时）白娘子传说发源地，登慈寿塔赏\"江天一览\"胜景\n🍜美食：镇江锅盖面（推荐肴肉面+水晶肴肉）\n🏨住宿：镇江精选经济型酒店（约200元/晚）\n\n**DAY2（10.2）镇江→常州**\n🚗交通：镇江→句容茅山（1小时）→常州环球恐龙城（1.5小时）\n📍景点：\n1. 【茅山景区】（3小时）道教圣地，乘索道登顶感悟\"第一福地\"\n2. 【环球恐龙城】（3小时）沉浸式恐龙主题乐园，夜游迪诺水镇灯光秀\n🍜美食：常州银丝面+蟹粉小笼包\n🏨住宿：常州精选商务酒店（约220元/晚）\n\n**DAY3（10.3）常州→无锡**\n🚗交通：常州→无锡鼋头渚（1.5小时）\n📍景点：\n1. 【鼋头渚】（4小时）太湖第一名胜，乘船观太湖仙岛，赏中秋明月\n2. 【蠡园】（2小时）范蠡西施传说地，江南园林典范\n🍜美食：太湖三白（银鱼/白虾/白鱼）\n🏨住宿：无锡梅里古镇亚朵酒店（参考价300元/晚）\n\n**DAY4（10.4）无锡深度游**\n📍景点：\n1. 【灵山胜境】（4小时）88米青铜大佛+梵宫精粹，参与中秋禅修体验\n2. 【惠山古镇】（3小时）千年祠堂建筑群，体验惠山泥人手作\n🍜美食：无锡小笼包+三凤桥酱排骨\n🏨住宿：美丽豪酒店（参考价280元/晚）\n\n**DAY5（10.5）返程**\n🚗交通：无锡→南京（2.5小时）\n📍景点：根据返程时间灵活调整，建议：\n- 无锡博物院（免费）了解吴文化\n- 南长街运河畔品早茶\n\n---\n\n**预算概算**\n💰总预算：1980元\n1. 交通：油费+过路费 300元\n2. 住宿：200+220+300+280=1000元\n3. 餐饮：60元/天×5=300元\n4. 门票：\n   - 栖霞山40+金山65+茅山120+恐龙城230+鼋头渚90+灵山210=755元\n   （注：提前1天网购享9折优惠，实付680元）\n\n---\n\n**行程亮点**\n1. 中秋特别体验：鼋头渚赏月专线+灵山抄经活动\n2. 错峰设计：首日避开南京热门景区，直达栖霞山赏初秋红叶\n3. 文化动线：金山寺→茅山→灵山构成宗教文化脉络\n\n建议携带汉服/旗袍在惠山古镇拍摄，无锡段行程可购买【文旅联票】享折扣。自驾注意沪宁高速节假日前夕拥堵，建议每日8:00前出发。');
INSERT INTO `main_route` VALUES (10, 1, '南京', '武汉', 2, '2000', '', '\n\n---\n\n### 🌟南京至武汉3天自驾游推荐方案（2025.9.24-9.26）\n\n---\n\n#### **行程整体概述**\n以 **“历史人文+自然风光”** 为主线，精选南京、安庆、武汉三地核心景点，全程自驾6小时，总预算控制在 **2000元内** 。行程安排松弛有度，兼顾文化体验与山水景观，特别标注【必打卡】与【本地特色】。\n\n---\n\n### **Day 1：南京文化深度游**\n**关键词**：明孝陵历史轴线｜秦淮河夜色｜老门东小吃  \n**交通**：南京市内自驾（无需长途驾驶）\n\n**08:30-12:00 钟山风景名胜区**  \n- **推荐理由**：南京必去“城市绿肺”，含明孝陵、中山陵、美龄宫三大核心，适合感受六朝古都的历史厚度（用户未指定偏好，默认覆盖多类型景点）。  \n- **玩法**：建议购买联票（约100元），重点游览【明孝陵神道】秋日梧桐，预计游玩3小时。  \n- **匹配需求**：古迹/森林/陵园多元素融合，满足泛文化游览需求。\n\n**12:30-13:30 午餐·南京大牌档（中山陵店）**  \n- **本地特色**：推荐盐水鸭、鸭血粉丝汤、赤豆元宵，人均60元，体验地道金陵风味。\n\n**14:00-17:00 夫子庙秦淮风光带**  \n- **推荐理由**：江南科举文化核心区，免费开放，可乘画舫夜游秦淮河（船票80元）。  \n- **隐藏玩法**：拐进老门东巷子，打卡先锋书店（骏惠书屋）和蒋有记锅贴。\n\n**18:00 住宿·南京清沐酒店（夫子庙店）**  \n- **推荐理由**：步行至夫子庙仅5分钟，经济型酒店约250元/晚，评分4.6，性价比高。\n\n---\n\n### **Day 2：山水穿越之旅（南京→安庆）**  \n**关键词**：天柱山地质奇观｜温泉疗愈  \n**交通**：自驾3小时（南京→安庆潜山市）\n\n**08:00-11:00 自驾前往天柱山**  \n- **沿途亮点**：途经马鞍山采石矶（可选停留1小时，门票60元），长江畔的“诗仙揽月处”。\n\n**12:00-13:00 午餐·潜山土菜馆**  \n- **必吃菜**：山粉圆子烧肉、痘姆古陶煨汤，人均40元，皖南农家风味。\n\n**13:30-17:30 天柱山主峰景区**  \n- **推荐理由**：世界地质公园，奇峰怪石云海三重奏，门票130元，缆车往返80元。  \n- **路线**：大龙窝索道→神秘谷→天池峰→炼丹湖，建议游玩4小时。\n\n**18:30 住宿·天悦湾温泉度假村**  \n- **推荐理由**：爬完山泡温泉（门票98元），缓解疲劳，酒店含双早约350元/晚。\n\n---\n\n### **Day 3：武汉都市漫游（安庆→武汉）**  \n**关键词**：黄鹤楼登高｜东湖骑行｜碳水狂欢  \n**交通**：自驾3小时（安庆→武汉）\n\n**08:00-11:00 自驾抵达武汉**  \n- **沿途彩蛋**：黄冈段可远眺大别山薄刀峰（免费观景台拍照）。\n\n**11:30-12:30 午餐·蔡林记（户部巷店）**  \n- **必吃榜**：热干面+蛋酒套餐（15元），武汉早餐文化代表。\n\n**13:00-15:00 黄鹤楼公园**  \n- **推荐理由**：江南四大名楼之一，门票70元，登楼俯瞰长江大桥，建议游玩2小时。  \n- **冷知识**：西门出可步行至武昌起义纪念馆（免费）。\n\n**15:30-18:00 东湖绿道骑行**  \n- **玩法**：扫共享单车沿湖中道骑行，免费开放，推荐落雁景区（婚纱摄影基地）。  \n\n**18:30 返程准备**  \n- **伴手礼**：周黑鸭锁鲜装（武汉站内有售），结束行程。\n\n---\n\n### **预算概算**（2人合计）  \n| 类别       | 明细                | 费用（元） |\n|------------|---------------------|------------|\n| **交通**   | 油费+过路费         | 500        |\n| **餐饮**   | 6正餐+小吃          | 600        |\n| **住宿**   | 南京1晚+安庆1晚     | 600        |\n| **门票**   | 天柱山+黄鹤楼等    | 500        |\n| **其他**   | 停车/零食/应急      | 200        |\n| **总计**   |                     | **2400**   |\n\n**省钱贴士**：天柱山周三免门票，黄鹤楼夜游票更便宜（若日期可调）。\n\n---\n\n### **⚠️重要提示**  \n1. 天柱山部分路段陡峭，建议穿防滑鞋；  \n2. 武汉限行政策需提前查车牌尾号；  \n3. 【关键时间】黄鹤楼17:00停止入场，东湖日落约18:10。\n\n---\n\n这份方案兼顾文化、自然与美食，预算微超但可通过调整餐饮或住宿档位优化。需要具体酒店比价或路线优化，随时告诉我！ 🚗✨');

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
