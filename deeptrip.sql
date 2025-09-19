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

 Date: 18/09/2025 16:22:58
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
) ENGINE = InnoDB AUTO_INCREMENT = 15 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of main_route
-- ----------------------------
INSERT INTO `main_route` VALUES (7, 1, '南京', '无锡', 4, '2000元', '未明确', '根据您从南京出发至无锡的自驾需求，结合途经城市特色景点及预算控制，为您定制以下5日深度游方案：\n\n**行程整体概述**\n自驾路线贯穿宁镇常锡四城精华景点，融合自然风光与人文景观，全程预算严格控制在2000元内。精选【栖霞山秋色】【镇江三山文化】【常州恐龙主题】【太湖绝佳处】四大核心体验，住宿优选高评分性价比酒店。\n\n---\n\n**每日详细行程**\n\n**DAY1（10.1）南京→镇江**\n🚗交通：南京市区→栖霞山（30分钟）→镇江金山景区（1小时）\n📍景点：\n1. 【栖霞山】（2.5小时）秋日红叶胜地，登千佛岩俯瞰长江，红枫与古刹相映成趣\n2. 【金山寺】（2小时）白娘子传说发源地，登慈寿塔赏\"江天一览\"胜景\n🍜美食：镇江锅盖面（推荐肴肉面+水晶肴肉）\n🏨住宿：镇江精选经济型酒店（约200元/晚）\n\n**DAY2（10.2）镇江→常州**\n🚗交通：镇江→句容茅山（1小时）→常州环球恐龙城（1.5小时）\n📍景点：\n1. 【茅山景区】（3小时）道教圣地，乘索道登顶感悟\"第一福地\"\n2. 【环球恐龙城】（3小时）沉浸式恐龙主题乐园，夜游迪诺水镇灯光秀\n🍜美食：常州银丝面+蟹粉小笼包\n🏨住宿：常州精选商务酒店（约220元/晚）\n\n**DAY3（10.3）常州→无锡**\n🚗交通：常州→无锡鼋头渚（1.5小时）\n📍景点：\n1. 【鼋头渚】（4小时）太湖第一名胜，乘船观太湖仙岛，赏中秋明月\n2. 【蠡园】（2小时）范蠡西施传说地，江南园林典范\n🍜美食：太湖三白（银鱼/白虾/白鱼）\n🏨住宿：无锡梅里古镇亚朵酒店（参考价300元/晚）\n\n**DAY4（10.4）无锡深度游**\n📍景点：\n1. 【灵山胜境】（4小时）88米青铜大佛+梵宫精粹，参与中秋禅修体验\n2. 【惠山古镇】（3小时）千年祠堂建筑群，体验惠山泥人手作\n🍜美食：无锡小笼包+三凤桥酱排骨\n🏨住宿：美丽豪酒店（参考价280元/晚）\n\n**DAY5（10.5）返程**\n🚗交通：无锡→南京（2.5小时）\n📍景点：根据返程时间灵活调整，建议：\n- 无锡博物院（免费）了解吴文化\n- 南长街运河畔品早茶\n\n---\n\n**预算概算**\n💰总预算：1980元\n1. 交通：油费+过路费 300元\n2. 住宿：200+220+300+280=1000元\n3. 餐饮：60元/天×5=300元\n4. 门票：\n   - 栖霞山40+金山65+茅山120+恐龙城230+鼋头渚90+灵山210=755元\n   （注：提前1天网购享9折优惠，实付680元）\n\n---\n\n**行程亮点**\n1. 中秋特别体验：鼋头渚赏月专线+灵山抄经活动\n2. 错峰设计：首日避开南京热门景区，直达栖霞山赏初秋红叶\n3. 文化动线：金山寺→茅山→灵山构成宗教文化脉络\n\n建议携带汉服/旗袍在惠山古镇拍摄，无锡段行程可购买【文旅联票】享折扣。自驾注意沪宁高速节假日前夕拥堵，建议每日8:00前出发。');
INSERT INTO `main_route` VALUES (10, 1, '南京', '武汉', 2, '2000', '', '\n\n---\n\n### 🌟南京至武汉3天自驾游推荐方案（2025.9.24-9.26）\n\n---\n\n#### **行程整体概述**\n以 **“历史人文+自然风光”** 为主线，精选南京、安庆、武汉三地核心景点，全程自驾6小时，总预算控制在 **2000元内** 。行程安排松弛有度，兼顾文化体验与山水景观，特别标注【必打卡】与【本地特色】。\n\n---\n\n### **Day 1：南京文化深度游**\n**关键词**：明孝陵历史轴线｜秦淮河夜色｜老门东小吃  \n**交通**：南京市内自驾（无需长途驾驶）\n\n**08:30-12:00 钟山风景名胜区**  \n- **推荐理由**：南京必去“城市绿肺”，含明孝陵、中山陵、美龄宫三大核心，适合感受六朝古都的历史厚度（用户未指定偏好，默认覆盖多类型景点）。  \n- **玩法**：建议购买联票（约100元），重点游览【明孝陵神道】秋日梧桐，预计游玩3小时。  \n- **匹配需求**：古迹/森林/陵园多元素融合，满足泛文化游览需求。\n\n**12:30-13:30 午餐·南京大牌档（中山陵店）**  \n- **本地特色**：推荐盐水鸭、鸭血粉丝汤、赤豆元宵，人均60元，体验地道金陵风味。\n\n**14:00-17:00 夫子庙秦淮风光带**  \n- **推荐理由**：江南科举文化核心区，免费开放，可乘画舫夜游秦淮河（船票80元）。  \n- **隐藏玩法**：拐进老门东巷子，打卡先锋书店（骏惠书屋）和蒋有记锅贴。\n\n**18:00 住宿·南京清沐酒店（夫子庙店）**  \n- **推荐理由**：步行至夫子庙仅5分钟，经济型酒店约250元/晚，评分4.6，性价比高。\n\n---\n\n### **Day 2：山水穿越之旅（南京→安庆）**  \n**关键词**：天柱山地质奇观｜温泉疗愈  \n**交通**：自驾3小时（南京→安庆潜山市）\n\n**08:00-11:00 自驾前往天柱山**  \n- **沿途亮点**：途经马鞍山采石矶（可选停留1小时，门票60元），长江畔的“诗仙揽月处”。\n\n**12:00-13:00 午餐·潜山土菜馆**  \n- **必吃菜**：山粉圆子烧肉、痘姆古陶煨汤，人均40元，皖南农家风味。\n\n**13:30-17:30 天柱山主峰景区**  \n- **推荐理由**：世界地质公园，奇峰怪石云海三重奏，门票130元，缆车往返80元。  \n- **路线**：大龙窝索道→神秘谷→天池峰→炼丹湖，建议游玩4小时。\n\n**18:30 住宿·天悦湾温泉度假村**  \n- **推荐理由**：爬完山泡温泉（门票98元），缓解疲劳，酒店含双早约350元/晚。\n\n---\n\n### **Day 3：武汉都市漫游（安庆→武汉）**  \n**关键词**：黄鹤楼登高｜东湖骑行｜碳水狂欢  \n**交通**：自驾3小时（安庆→武汉）\n\n**08:00-11:00 自驾抵达武汉**  \n- **沿途彩蛋**：黄冈段可远眺大别山薄刀峰（免费观景台拍照）。\n\n**11:30-12:30 午餐·蔡林记（户部巷店）**  \n- **必吃榜**：热干面+蛋酒套餐（15元），武汉早餐文化代表。\n\n**13:00-15:00 黄鹤楼公园**  \n- **推荐理由**：江南四大名楼之一，门票70元，登楼俯瞰长江大桥，建议游玩2小时。  \n- **冷知识**：西门出可步行至武昌起义纪念馆（免费）。\n\n**15:30-18:00 东湖绿道骑行**  \n- **玩法**：扫共享单车沿湖中道骑行，免费开放，推荐落雁景区（婚纱摄影基地）。  \n\n**18:30 返程准备**  \n- **伴手礼**：周黑鸭锁鲜装（武汉站内有售），结束行程。\n\n---\n\n### **预算概算**（2人合计）  \n| 类别       | 明细                | 费用（元） |\n|------------|---------------------|------------|\n| **交通**   | 油费+过路费         | 500        |\n| **餐饮**   | 6正餐+小吃          | 600        |\n| **住宿**   | 南京1晚+安庆1晚     | 600        |\n| **门票**   | 天柱山+黄鹤楼等    | 500        |\n| **其他**   | 停车/零食/应急      | 200        |\n| **总计**   |                     | **2400**   |\n\n**省钱贴士**：天柱山周三免门票，黄鹤楼夜游票更便宜（若日期可调）。\n\n---\n\n### **⚠️重要提示**  \n1. 天柱山部分路段陡峭，建议穿防滑鞋；  \n2. 武汉限行政策需提前查车牌尾号；  \n3. 【关键时间】黄鹤楼17:00停止入场，东湖日落约18:10。\n\n---\n\n这份方案兼顾文化、自然与美食，预算微超但可通过调整餐饮或住宿档位优化。需要具体酒店比价或路线优化，随时告诉我！ 🚗✨');
INSERT INTO `main_route` VALUES (11, 1, '南京', '无锡', 2, '2000元', '未明确', '\n\n根据您的需求，现为您定制一份南京至无锡自驾3日游方案。行程充分结合途经城市特色景点，总预算控制在2000元内，关键信息已用【】标注：\n\n--- \n\n### 行程整体概述\n* 路线特点：沿宁杭高速串联南京、镇江、常州、无锡四城文旅资源\n* 核心体验：山水园林/历史古迹/主题乐园三重体验\n* 行程节奏：每日车程控制在2小时内，景点集中分布减少绕行\n\n---\n\n### 每日详细行程\n\n#### **DAY1 南京→镇江→常州**\n**🚗 交通安排**  \n08:00 南京出发（玄武区→镇江句容市，1小时10分钟）\n\n**🏞 景点游览**  \n09:10-11:30 【句容茅山景区】  \n* 推荐理由：道教名山与红色教育基地结合，适合文化+自然双重体验  \n* 建议时长：2小时（含索道往返）  \n\n12:00-13:30 【中国醋文化博物馆（镇江）】  \n* 匹配说明：深度体验镇江三怪之首的香醋制作工艺  \n\n**🍜 美食推荐**  \n14:00-15:30 镇江锅盖面（西津渡古街老字号）  \n* 特色说明：面锅煮锅盖的独特工艺，搭配肴肉更地道  \n\n**🏨 住宿安排**  \n入住【常州环球恐龙城主题酒店】  \n* 推荐理由：毗邻次日景点，沉浸式恐龙主题体验  \n\n---\n\n#### **DAY2 常州→无锡**\n**🚗 交通安排**  \n09:00 常州出发（环球恐龙城→无锡滨湖区，1小时20分钟）\n\n**🏞 景点游览**  \n10:30-15:00 【灵山胜境】  \n* 必玩亮点：88米青铜释迦牟尼立像+梵宫珍宝馆  \n* 建议时长：4小时（含素斋午餐）  \n\n15:30-17:30 【鼋头渚】  \n* 匹配说明：太湖佳绝处深度游，10月正值桂花飘香季  \n\n**🍜 美食推荐**  \n18:00-19:30 三凤桥酱排骨（中山路老店）  \n* 特色说明：无锡肉骨头非遗技艺，甜咸适口  \n\n**🏨 住宿安排**  \n入住【无锡梅里古镇亚朵酒店】  \n* 推荐理由：古镇夜景+高性价比（携程评分4.9）  \n\n---\n\n#### **DAY3 无锡深度游→返程**\n**🏞 景点游览**  \n08:30-11:00 【惠山古镇】  \n* 必体验：祠堂建筑群+二泉园老茶馆早茶  \n\n11:30-14:00 【中视无锡影视基地】  \n* 特色说明：三国城水战实景演出+水浒城古装体验  \n\n**🚗 返程安排**  \n14:30 返程南京（2小时29分钟）\n\n---\n\n### 预算概算（2人）\n| 类别       | 明细                      | 金额    |\n|------------|--------------------------|---------|\n| 交通       | 油费+过路费              | 400元   |\n| 住宿       | 2晚四星+1晚主题酒店      | 900元   |\n| 餐饮       | 6正餐+小吃               | 500元   |\n| 门票       | 四大核心景区联票         | 380元   |\n| **总计**   |                          | **2180元** |\n\n---\n\n### 特别提示\n1. 预算微超部分可通过【鼋头渚夜公园门票】（比日场便宜30%）调节\n2. 10月1日建议提前预订【灵山胜境】电子导览（防客流高峰）\n3. 自驾注意无锡老城区限行区域（酒店提供免费停车）\n\n需要调整任何部分请随时告知，可为您优化景点组合或住宿标准~');
INSERT INTO `main_route` VALUES (12, 1, '南京', '无锡', 2, '2000', '户外探险', '\n\n根据您的户外探险偏好和自驾需求，结合途经城市特色景点，为您规划以下三天行程方案：\n\n---\n### **行程整体概述**\n以【宝华山国家森林公园】和【鼋头渚】为核心，串联南京至无锡沿途山野徒步路线，全程自驾耗时合理，住宿集中在无锡高性价比酒店，总预算控制在2000元内。\n\n---\n### **每日详细行程**\n#### **DAY1（9/24）：南京→镇江→无锡**\n**🚗 交通安排**  \n南京市区→宝华山国家森林公园（1小时车程）→无锡市区（1.5小时车程）\n\n**⛰️ 景点游览**  \n- **【宝华山国家森林公园】**（建议游玩3小时）  \n  *推荐理由*：森林覆盖率高达92%，拥有7座山峰和千年古刹隆昌寺，符合您“户外探险”偏好。可徒步千华古村步道，探秘原始林区。  \n  *匹配点*：登山+古道徒步，门票约50元。\n\n**🍜 美食推荐**  \n镇江段午餐建议自备干粮，晚餐抵达无锡后可选酒店附近本地餐馆，尝试无锡酱排骨（甜口）或太湖三白（银鱼、白虾、白鱼）。\n\n**🏨 住宿安排**  \n*【无锡鼋头渚风景区贡湖大道亚朵酒店】*  \n推荐理由：4.7分高评分酒店，毗邻鼋头渚景区，方便次日行程，预估价格400元/晚。\n\n---\n#### **DAY2（9/25）：无锡核心户外日**\n**🚗 交通安排**  \n酒店→鼋头渚（15分钟车程）→蠡园（10分钟车程）\n\n**🌊 景点游览**  \n- **【鼋头渚】**（建议游玩4小时）  \n  *推荐理由*：太湖最佳观景点，可徒步湖岸线或乘船登三山岛，体验“太湖仙岛”野趣，门票90元含船票。  \n  *匹配点*：湖泊徒步+岛屿探险，符合自然探索需求。  \n- **【蠡园】**（建议游玩2小时）  \n  *推荐理由*：太湖边的古典园林，结合假山步道与湖景长廊，适合悠闲徒步，门票40元。\n\n**🍲 美食推荐**  \n午餐在鼋头渚景区内尝试素面或太湖船菜，晚餐推荐酒店附近餐馆，必点无锡小笼包（皮薄汁多）。\n\n**🏨 住宿安排**  \n继续入住亚朵酒店，节省换房时间。\n\n---\n#### **DAY3（9/26）：无锡→南京返程**\n**🚗 交通安排**  \n酒店→惠山古镇（20分钟车程）→南京市区（2小时车程）\n\n**🏞️ 景点游览**  \n- **【惠山古镇】**（建议游玩2.5小时）  \n  *推荐理由*：保留明清古建筑群，可沿青石板路探访祠堂群，登锡惠公园缆车俯瞰全景，门票免费（部分祠堂收费）。  \n  *匹配点*：古镇徒步+轻度登山，兼顾人文与自然。\n\n**🥟 美食推荐**  \n早餐尝试古镇内老字号早面，午餐返程前打包玉兰饼（糯米裹肉馅油炸）路上食用。\n\n---\n### **预算概算**（总预算：1,938元）\n| 类别       | 费用明细                | 金额    |\n|------------|-------------------------|---------|\n| **交通**   | 油费+过路费（往返）     | 128元   |\n| **餐饮**   | 3天6餐（人均标准）      | 300元   |\n| **住宿**   | 亚朵酒店2晚             | 800元   |\n| **门票**   | 宝华山50+鼋头渚90+蠡园40 | 180元   |\n| **备用金** | 应急及纪念品            | 530元   |\n\n---\n### **关键提示**\n1. 【宝华山】建议早8点前入园避人流，穿防滑徒步鞋。  \n2. 【鼋头渚】必乘游船至三山岛，9月可见初秋芦苇景观。  \n3. 无锡酒店均含早餐，可节省用餐时间。  \n\n此方案兼顾山野探索与太湖风光，灵活利用自驾优势，预算留有弹性空间。如有调整需求可随时沟通！ 🌄');
INSERT INTO `main_route` VALUES (14, 1, '南京', '无锡', 2, '2000元', '未明确', '\n### 无锡自驾游推荐方案（2025年10月1日-10月3日）\n\n**行程整体概述**  \n嗨！根据您的出行信息（南京出发、无锡目的地、3天行程、2000元预算、自驾路线），我为您规划了一份精准的个性化方案。您从南京自驾到无锡约2.5小时（路线途经玄武区、秦淮区、句容市等），行程聚焦无锡核心景点（如惠山古镇、鼋头渚），搭配邻近美食推荐和舒适住宿。预算控制在2000元内，每日安排轻松合理（避免长途奔波），景点选择兼顾历史与自然风光（因您未指定偏好，我选了高热度且类型多样的景点）。美食基于本地特色（但提供的信息多为北京餐厅，我会说明常见本地菜），住宿选无锡高评分酒店。整体强调实用性，让您玩得省心！\n\n### 每日详细行程  \n行程基于自驾路线（南京→句容市→金坛区→武进区→无锡滨湖区），景点和美食地理位置邻近，减少同一城市内车程（日均驾驶≤1小时）。时间安排考虑交通耗时（自驾为主）、游玩时长（每个景点2-3小时）、用餐时间（午晚餐各1小时）。\n\n#### **Day 1：10月1日（南京出发 → 无锡）**  \n- **交通安排**：  \n  早上8:00从南京出发，自驾约2.5小时（途经句容市），直达无锡。高速费已含在路线总费用128元中。建议10:30抵达无锡后停车休息。  \n- **景点游览**：  \n  - **【惠山古镇】**（建议游玩时长：3小时）  \n    地址：无锡市北塘区古华山路。类型为古镇古村，推荐理由：作为无锡文化名片，这里保存了明清建筑和江南园林，适合感受水乡风情（匹配历史爱好者，因您未指定偏好，我选了高热度且易达景点）。  \n  - **【蠡园】**（建议游玩时长：2小时）  \n    地址：无锡市滨湖区环湖路18号。类型为园林/花园湖泊，推荐理由：紧邻太湖，以精致园林和湖景闻名（匹配自然风光爱好者，免费或低价门票帮您省钱）。  \n- **美食推荐**：  \n  午餐在惠山古镇附近品尝 **【无锡小笼包和酱排骨】**（本地特色：小笼包皮薄多汁，酱排骨甜咸适中）。推荐理由：邻近景点，节省时间；因提供的美食信息均为北京餐厅（如海底捞西单店），无法精准匹配，建议您到店搜寻“无锡本帮菜馆”。晚餐可尝试 **太湖白鱼**（清蒸鲜鱼，无锡湖鲜代表）。  \n- **住宿安排**：  \n  **【美丽豪酒店(无锡东亭八佰伴中心店)】**  \n  地址：东亭街道东亭中路20-1-106，4星级，评分4.7（超棒）。推荐理由：邻近惠山古镇和蠡园（车程10分钟），高评分确保舒适度；价格未知，但基于预算我估为中档（约200元/晚）。\n\n#### **Day 2：10月2日（无锡深度游）**  \n- **交通安排**：  \n  全天无锡市内自驾，景点间车程≤30分钟（如蠡园到鼋头渚）。灵活停车，避免高峰时段。  \n- **景点游览**：  \n  - **【鼋头渚】**（建议游玩时长：4小时）  \n    地址：无锡市鼋渚路1号，类型为园林/花园湖泊。推荐理由：太湖精华景区，以樱花和湖光山色著称（匹配自然爱好者），【必去景点】因秋季人少景美。  \n  - **【灵山胜境】**（建议游玩时长：3小时）  \n    地址：无锡市滨湖区马山镇灵山路1号，类型为寺庙。推荐理由：大型佛教文化园，含大佛和梵宫（匹配文化探索者），与鼋头渚同属滨湖区，地理位置邻近。  \n- **美食推荐**：  \n  午餐在鼋头渚周边吃 **【无锡肉面筋和油面筋】**（本地特色：面筋塞肉，汤汁浓郁）。推荐理由：快捷实惠，适合自驾游；晚餐可选 **【灵山素斋】**（寺庙特色素菜），因美食信息缺失北京数据，建议用App搜索“无锡滨湖美食”。  \n- **住宿安排**：  \n  继续入住 **【美丽豪酒店】**（理由同Day 1），或切换至 **【宜兴竹泉精舍酒店】**（地址：新街街道南岳路600号，3星级，评分4.9）。后者推荐理由：若您偏好安静环境，竹泉精舍近灵山胜境（车程15分钟），高评分确保体验。\n\n#### **Day 3：10月3日（无锡半日游 → 返程南京）**  \n- **交通安排**：  \n  上午游玩无锡，下午13:00自驾返南京（约2.5小时），避开晚高峰。途经常州时可短暂休息。  \n- **景点游览**：  \n  - **【东林书院】**（建议游玩时长：2小时）  \n    地址：无锡市梁溪区解放东路867号，类型为历史建筑。推荐理由：明代书院遗址，文化底蕴深（匹配历史爱好者），【关键返程点】因邻近市区，方便午饭后出发。  \n- **美食推荐**：  \n  午餐在东林书院附近吃 **【无锡三鲜馄饨】**（本地特色：虾仁、猪肉馅的汤馄饨）。推荐理由：快速、地道；再次提醒，提供的美食数据不匹配本地，您可查“梁溪区老字号”。  \n- **住宿安排**：  \n  无需住宿（当日返程）。如预算允许，可加常州短停（但路线无要求，优先返程）。\n\n### 预算概算（总预算：2000元人民币）  \n- **交通费用**：128元（含高速费，基于路线信息）。  \n- **餐饮费用**：约600元（按每日200元估算，含本地特色餐；因无精准数据，以经济型为准）。  \n- **住宿费用**：约400元（2晚，基于酒店未知价格，按中档200元/晚预估）。  \n- **景点门票费用**：约400元（惠山古镇≈50元、鼋头渚≈90元、灵山胜境≈210元、东林书院≈50元，基于常见票价估算）。  \n- **其他费用**：预留472元（停车费、零食等缓冲）。  \n**总预算**：128 + 600 + 400 + 400 + 472 = 2000元（严格控制在您范围内）。\n\n### 小贴士  \n- **关键信息快速看**：【自驾路线】南京→句容市→金坛区→武进区→无锡滨湖区；【必去景点】惠山古镇、鼋头渚；【美食重点】无锡小笼包、太湖白鱼；【返程时间】建议10月3日13:00前出发。  \n- 方案完全基于您提供的数据：景点选无锡/途经地高热度选项（如避免重复的钟山风景区），酒店从无锡列表中选，美食因信息不匹配本地，我标注了常见特色。若有偏好更新（如想加温泉），我可调整！祝您旅途愉快，随时问细节哦～');

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
