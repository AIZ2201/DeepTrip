from openai import OpenAI
from typing import List  # 需导入List用于类型声明
from ..gaode_agent.agent import GaodeAgent
from datetime import datetime
from ..gaode_agent.agent import parse_gaode_result
from ..xiecheng_agent.agent import XiechengAgent
from ..food_agent.agent import Agent as FoodAgent
from ..tourism_agent.agent import Agent as TourismAgent
from agent.xiecheng_agent.agent import XiechengAgent
from .dataclass import (
    UserTravelPreference, 
    TravelRoute,  # 导入单个路线的数据类
    TravelRouteList,
    HotelOption, 
    HotelOptionList,
    LandmarkOption, 
    FoodOption
)
from .key_point_extract import key_point_extract

class ChatAgent:
    def __init__(self):
        self.gaode_agent = GaodeAgent()
        self.xiecheng_agent = XiechengAgent()
        self.food_agent = FoodAgent() 
        self.tourism_agent = TourismAgent()
        # 初始化用户旅游信息（空实例）
        self.user_travel_info = UserTravelPreference(
            departure_city="",
            destination_city="",
            start_date="",
            end_date="",
            budget="",
            spot_preference=[],
            hotel_preference=[],
            special_needs=[]
        )
        # 初始化路线列表容器（空路线列表）
        self.travel_route_list = TravelRouteList(
            routes=[],
            recommend_route_index=0,
            start_city="",
            end_city=""
        )
        # 初始化餐饮
        self.food_options: List[FoodOption] = []
        # 初始化景点
        self.landmark_options: List[LandmarkOption] = []
        
        self.hotel_option_list = HotelOptionList(
            hotels=[],
            sort_type="",
            total_count=0,
            destination_city="",
            check_in_date="",
            check_out_date="",
            recommend_hotel_index=0
        )
        # 初始化LLM客户端（完全按照你的调用方式）
        self.llm_client = OpenAI(
            api_key="sk-31PqbF5zvpyDAbAYB1XrIu6d5eZpdjx3PyvHzM6Vab8RdrGS",
            base_url="https://api.chatanywhere.tech/v1",
        )
    

    def get_travel_info(self, travel_dict: dict) -> UserTravelPreference:
        """根据提取的travel_dict，更新用户旅游信息（self.user_travel_info）"""
        self.user_travel_info = UserTravelPreference(
            departure_city=travel_dict.get("出发点", ""),
            destination_city=travel_dict.get("目的地", ""),
            start_date=travel_dict.get("行程时间", {}).get("入住日期", ""),
            end_date=travel_dict.get("行程时间", {}).get("离店日期", ""),
            budget=travel_dict.get("经费预算", ""),
            spot_preference=travel_dict.get("景点类型偏好", []),
            hotel_preference=travel_dict.get("住宿需求", []),
            special_needs=travel_dict.get("特殊需求", [])
        )
        return self.user_travel_info




    def get_path_info(self) -> TravelRouteList:
        """
        根据出发地/目的地，调用高德Agent获取路线，更新self.travel_route_list
        :param start_city: 起点城市（如“南京市”）
        :param end_city: 终点城市（如“武汉市”）
        :return: 更新后的TravelRouteList实例
        """
        start_city = self.user_travel_info.departure_city
        end_city = self.user_travel_info.destination_city
        # 1. 基础校验：起点/终点不能为空
        if not start_city or not end_city:
            print(f"错误：起点城市（{start_city}）或终点城市（{end_city}）不能为空")
            return self.travel_route_list  # 返回空容器，避免后续报错

        try:
            # 2. 调用高德Agent获取原始路线数据（path_info为高德API返回的字典）
            path_info = self.gaode_agent.get_path(start_city, end_city)
            if not path_info:
                print("获取高德路线原始数据失败")
                return self.travel_route_list

            # 3. 解析原始数据为List[dict]（复用gaode_agent的parse_gaode_result方法）
            all_routes = parse_gaode_result(path_info)
            # 过滤错误数据（如“无有效路径数据”的情况）
            valid_routes = [route for route in all_routes if "error" not in route]
            if not valid_routes:
                print(f"无有效路线数据：{all_routes[0].get('error', '未知错误')}")
                return self.travel_route_list

            # 4. 将List[dict]转为TravelRoute实例列表
            travel_route_list: List[TravelRoute] = []
            for route_dict in valid_routes:
                # 逐个字段映射，确保类型匹配（如红绿灯数量为int）
                travel_route = TravelRoute(
                    total_time=route_dict.get("总耗时", "未知耗时"),
                    total_cost=route_dict.get("总收费", "0.00元"),
                    toll_mileage=route_dict.get("收费里程", "0公里"),
                    traffic_light_count=route_dict.get("红绿灯数量", 0),  # 确保int类型
                    passing_areas=route_dict.get("途经城市/区县", []),  # 确保List[str]类型
                    route_type="自驾",  # 默认为自驾（可根据高德返回扩展其他类型）
                    start_point=start_city,  # 同步起点城市
                    end_point=end_city       # 同步终点城市
                )
                travel_route_list.append(travel_route)

            # 5. 计算推荐路线索引（按“总耗时最短”推荐）
            def get_time_minutes(time_str: str) -> int:
                """辅助函数：将“X小时Y分钟”转为总分钟数，用于排序"""
                hour = int(time_str.split("小时")[0]) if "小时" in time_str else 0
                minute = int(time_str.split("小时")[-1].replace("分钟", "")) if "分钟" in time_str else 0
                return hour * 60 + minute

            # 按耗时升序排序，取第一条路线的索引作为推荐索引
            if travel_route_list:
                # 排序后的路线列表（按耗时从短到长）
                sorted_routes = sorted(travel_route_list, key=lambda x: get_time_minutes(x.total_time))
                # 找到推荐路线在原始列表中的下标（从0开始）
                recommend_index = travel_route_list.index(sorted_routes[0])
            else:
                recommend_index = 0  # 无路线时默认索引0

            # 6. 更新self.travel_route_list（路线容器）
            self.travel_route_list = TravelRouteList(
                routes=travel_route_list,
                recommend_route_index=recommend_index,
                start_city=start_city,
                end_city=end_city
            )
            return self.travel_route_list  # 返回更新后的路线列表容器
            print(f"成功获取{len(travel_route_list)}条路线，推荐路线索引：{recommend_index}")

        except Exception as e:
            # 捕获异常，避免程序崩溃
            print(f"获取路线信息时发生错误：{str(e)}")

    def get_hotel_info(self, top_n: int = 5) -> HotelOptionList:
        """调用XiechengAgent，将返回的字典列表转为HotelOptionList"""
        # 1. 从用户偏好获取必要参数
        dest_city = self.user_travel_info.destination_city  # 如"哈尔滨"
        check_in = self.user_travel_info.start_date         # 如"20250915"
        check_out = self.user_travel_info.end_date          # 如"20250917"
        city_id,province_id = self._get_city_id(dest_city)              # 如哈尔滨city_id=5
        

        # 2. 校验参数
        if not (dest_city and check_in and check_out and city_id and province_id) or city_id == -1 or province_id == -1:
            print("参数不全：需先获取用户的目的地、日期及对应城市ID/省份ID")
            return self.hotel_option_list

        try:
            # 3. 调用你的XiechengAgent获取酒店字典列表
            sorted_hotels = self.xiecheng_agent.get_hotels(
                city_id=city_id,
                province_id=province_id,
                check_in_date=check_in,
                check_out_date=check_out,
                top_n=top_n
            )
            if not sorted_hotels:
                print("XiechengAgent未返回有效酒店数据")
                return self.hotel_option_list

            # 4. 将字典列表转为HotelOption实例列表（核心映射）
            hotel_options: List[HotelOption] = []
            for hotel_dict in sorted_hotels:
                hotel_option = HotelOption(
                    name=hotel_dict["name"],
                    address=hotel_dict["address"],
                    star=hotel_dict["star_level"],  # 直接用格式化后的"4星"
                    score=hotel_dict["score"],
                    hotel_image_url=hotel_dict["appearance_img_url"],
                    star_image_url=hotel_dict["star_icon_url"],
                    price=hotel_dict["price"]  # 已处理"未知价格"情况
                )
                hotel_options.append(hotel_option)

            # 5. 计算推荐酒店索引（示例：优先选评分高+价格低的）
            def recommend_strategy(hotel: HotelOption) -> tuple:
                # 评分转为浮点数（如"4.8 (超棒)"→4.8），价格转为浮点数（如"588元"→588）
                score_val = float(hotel.score.split(" ")[0]) if hotel.score.replace(".", "").isdigit() else 0
                price_val = float(hotel.price.replace("元", "")) if (hotel.price != "未知价格" and hotel.price.replace("元", "").isdigit()) else float("inf")
                return (-score_val, price_val)  # 负评分（降序）、价格（升序）

            # 按策略排序，取第一个作为推荐酒店
            recommended_hotel = sorted(hotel_options, key=recommend_strategy)[0]
            recommend_index = hotel_options.index(recommended_hotel)

            # 6. 封装为HotelOptionList
            self.hotel_option_list = HotelOptionList(
                hotels=hotel_options,
                sort_type="按价格升序",  # 你的XiechengAgent已按价格排序
                total_count=len(hotel_options),
                destination_city=dest_city,
                check_in_date=check_in,
                check_out_date=check_out,
                recommend_hotel_index=recommend_index
            )
            print(f"成功映射{len(hotel_options)}家酒店到数据类")

        except Exception as e:
            print(f"酒店数据映射失败：{str(e)}")

        return self.hotel_option_list
    
    def _get_city_id(self, city_name: str) -> tuple[int,int]:
        """
        根据城市名称获取城市ID和省份ID
        :param city_name: 城市名称，如"哈尔滨"
        :return: (city_id, province_id)，找不到时返回(-1, -1)
        """
        city_id, province_id = self.xiecheng_agent.get_city_id(city_name)
        return city_id, province_id
    

    def get_food_info(self, keywords: str = "美食"):
        """
        根据关键词获取美食信息，调用food_agent进行批量查询，并将结果存入self.food_options
        :param keywords: 美食关键词（如"美食"）
        :return: 更新后的self.food_options列表
        """
        try:
            # 检查推荐路线是否存在
            if not self.travel_route_list.routes:
                print("错误：没有可用的路线信息")
                return []
            
            # 获取推荐路线的途经城市
            idx = self.travel_route_list.recommend_route_index
            recommend_route = self.travel_route_list.routes[idx]
            passing_areas = recommend_route.passing_areas
            
            if not passing_areas:
                print("错误：推荐路线没有途经城市信息")
                return []
            
            # 准备批量查询的城市列表
            cities_to_search = []
            # 确保途经城市是列表类型
            if isinstance(passing_areas, str):
                # 将城市名中的"-"替换为"·"
                formatted_city = passing_areas.replace("-", "")
                cities_to_search = [formatted_city]
            # 处理城市列表
            elif isinstance(passing_areas, list):
                cities_to_search = [city.replace("-", "") for city in passing_areas]
            else:
                cities_to_search = []
                print(f"Invalid passing_areas type: {type(passing_areas)}")
            
            # 调用food_agent进行批量查询
            print(f"正在批量查询以下城市的美食信息: {', '.join(cities_to_search)}")
            food_result = self.food_agent.batch_search_food_by_keyword(
                cities=cities_to_search,
                keyword=keywords,
                delay=0.5
            )
            
            # 检查查询结果是否成功
            if not food_result or "food_list" not in food_result:
                print("错误：获取美食信息失败")
                return []
            
            # 清空之前的美食信息
            self.food_options = []
            
            # 将查询结果转换为FoodOption对象
            for food_item in food_result["food_list"]:
                # 处理评分（从float转为str）
                score_str = str(food_item.get("score", 0.0))
                
                # 处理推荐菜品（从list转为str）
                recommend_list = food_item.get("recommend", [])
                recommend_str = ", ".join(recommend_list) if isinstance(recommend_list, list) else str(recommend_list)
                
                tel_list = food_item.get("tel", [])
                tel_str = ", ".join(tel_list) if isinstance(tel_list, list) else str(tel_list)

                # 创建FoodOption对象
                food_option = FoodOption(
                    name=food_item.get("name", "未知名称"),
                    score=score_str,
                    address=food_item.get("address", "未知地址"),
                    type=food_item.get("type", "未知类型"),
                    area=food_item.get("area", "未知区域"),
                    tel=tel_str,
                    recommend=recommend_str
                )
                
                self.food_options.append(food_option)
            
            print(f"成功获取并转换了{len(self.food_options)}条美食信息")
            return self.food_options
            
        except Exception as e:
            print(f"获取美食信息时发生错误：{str(e)}")
            self.food_options = []
            return []
        

    def get_tourism_info(self):
        """
        获取景点信息，调用tourism_agent进行批量查询，并将结果存入self.landmark_options
        :return: 更新后的self.landmark_options列表
        """
        try:
            # 检查推荐路线是否存在
            if not self.travel_route_list.routes:
                print("错误：没有可用的路线信息")
                return []
            
            # 获取推荐路线的途经城市
            idx = self.travel_route_list.recommend_route_index
            recommend_route = self.travel_route_list.routes[idx]
            passing_areas = recommend_route.passing_areas
            
            if not passing_areas:
                print("错误：推荐路线没有途经城市信息")
                return []
            
            # 准备批量查询的城市列表
            areas_to_search = []
            if isinstance(passing_areas, str):
                # 将城市名中的"-"替换为"·"
                formatted_city = passing_areas.replace("-", "·")
                areas_to_search = [formatted_city]
            # 处理城市列表
            elif isinstance(passing_areas, list):
                areas_to_search = [city.replace("-", "·") for city in passing_areas]
            else:
                areas_to_search = []
                print(f"Invalid passing_areas type: {type(passing_areas)}")
            
            # 调用tourism_agent进行批量查询，合并结果并按热度排序
            print(f"正在批量查询以下地区的景点信息: {', '.join(areas_to_search)}")
            tourism_result = self.tourism_agent.batch_search_scenic_spots(
                area_list=areas_to_search,
                page=1,
                delay=0.5,
                merge_results=True,
                sort_by_hot=True
            )
            
            # 检查查询结果是否成功
            if not tourism_result or "scenic_spots" not in tourism_result:
                print("错误：获取景点信息失败")
                return []
            
            # 清空之前的景点信息
            self.landmark_options = []
            
            # 将查询结果转换为LandmarkOption对象
            for spot_item in tourism_result["scenic_spots"]:
                # 处理热度（从float转为str）
                hot_value = spot_item.get("hot", 0.0)
                hot_str = f"热度 {hot_value}"
                
                # 构建景点区域信息
                area_str = spot_item.get("area", "未知区域")
                # 如果有来源地区信息，添加到区域中
                if "source_area" in spot_item:
                    area_str = f"{spot_item['source_area']}-{area_str}"
                
                # 创建LandmarkOption对象
                landmark_option = LandmarkOption(
                    area=area_str,
                    name=spot_item.get("name", "未知景点"),
                    level=spot_item.get("level", "无等级"),
                    address=spot_item.get("address", "未知地址"),
                    type=spot_item.get("type", "未知类型"),
                    intro=spot_item.get("intro", "暂无介绍"),
                    hot=hot_str
                )
                
                self.landmark_options.append(landmark_option)
            
            print(f"成功获取并转换了{len(self.landmark_options)}个景点信息")
            return self.landmark_options
            
        except Exception as e:
            print(f"获取景点信息时发生错误：{str(e)}")
            self.landmark_options = []
            return []
        
    def generate_comprehensive_travel_plan(self) -> str:
        """
        整合所有信息，使用指定的LLM调用方式生成完整旅游规划
        完全适配你的API Key配置和参数风格
        """
        # 1. 数据有效性检查
        missing_info = []
        if not self.user_travel_info.destination_city:
            missing_info.append("用户目的地城市")
        if not self.travel_route_list.routes:
            missing_info.append("推荐路线")
        if not self.landmark_options:
            missing_info.append("沿途景点")
        if not self.food_options:
            missing_info.append("沿途美食")
        if not self.hotel_option_list.hotels:
            missing_info.append("目的地酒店")
        
        if missing_info:
            return f"❌ 无法生成完整旅游规划，缺少以下关键信息：{', '.join(missing_info)}"

        # 2. 整理所有信息为LLM可理解的格式
        plan_info = self._prepare_plan_information()

        # 3. 构建消息列表（遵循你的messages格式）
        messages = [
            {"role": "system", "content": self._get_system_prompt()},
            {"role": "user", "content": plan_info}
        ]

        try:
            # 4. 调用LLM（完全按照你的参数风格）
            completion = self.llm_client.chat.completions.create(
                model="deepseek-r1",  # 使用你指定的模型
                messages=messages,
                temperature=0.3,  # 低随机性，保持规划严谨
                max_tokens=2000,  # 足够生成详细规划
                top_p=1,
                frequency_penalty=0.2,
                presence_penalty=0.2
            )
            
            return completion.choices[0].message.content
        
        except Exception as e:
            print(f"LLM调用出错: {str(e)}")
            return self._generate_fallback_plan()

    def _get_system_prompt(self) -> str:
        """优化后的系统提示词，明确基于所有搜集信息生成推荐"""
        return """你是一位专业且经验丰富的旅游规划师，现在需要基于用户的出行信息，以及我们为你搜集到的酒店、美食、景点等详细信息，为用户生成一份精准且个性化的旅游推荐方案。请严格遵循以下要求：

            1. 【信息利用要求】
            - 必须完全基于提供的用户出行信息、酒店信息、美食信息、景点信息来生成推荐，不得引入其他外部信息。
            - 充分考虑用户的各项偏好（如景点类型偏好、住宿需求、特殊需求等），在推荐时进行匹配说明。

            2. 【内容结构要求】
            - 整体方案需包含：行程整体概述、每日详细行程（交通安排、景点游览、美食推荐、住宿安排）、预算概算等部分。
            - 每日行程要按照“交通安排→景点游览（含推荐理由及与用户偏好的匹配点、建议游玩时长）→美食推荐（含本地特色说明及推荐理由）→住宿安排（含推荐理由）”的顺序组织。
            - 预算概算部分货币单位统一为人民币，分类清晰（如交通费用、餐饮费用、住宿费用、景点门票费用等）。
            - 关键信息（如必去景点、特色美食、重要时间节点等）用【】标注，方便用户快速查看。

            3. 【行程合理性要求】
            - 每日行程的时间安排要合理，充分考虑交通耗时、景点游玩时长、用餐时间等，符合实际旅行节奏。
            - 景点与美食的地理位置要邻近，避免同一城市内不必要的远距离往返。
            - 行程整体要与推荐路线的进度相匹配，不能出现与路线无关的城市或地点推荐。

            4. 【语言风格要求】
            - 语言表达要自然、友好、口语化，避免使用过于专业或生硬的术语。
            - 解释推荐理由时要结合用户的具体偏好，让用户清楚了解推荐的依据。

            请根据以上要求，生成一份让用户感觉“精准匹配自身需求且实用”的旅游推荐方案。"""

    def _prepare_plan_information(self) -> str:
        """更清晰、完整地整理所有信息传递给大模型"""
        # 计算行程天数
        def calc_days():
            try:
                start = datetime.strptime(self.user_travel_info.start_date, "%Y%m%d")
                end = datetime.strptime(self.user_travel_info.end_date, "%Y%m%d")
                return (end - start).days + 1
            except:
                return 1

        # 用户出行信息
        user_info = f"""
        【用户出行信息】
        - 出发城市：{self.user_travel_info.departure_city}
        - 目的城市：{self.user_travel_info.destination_city}
        - 行程时间：{self.user_travel_info.start_date} 至 {self.user_travel_info.end_date}（共{calc_days()}天）
        - 预算范围：{self.user_travel_info.budget or '未明确，可适当灵活调整'}
        - 景点类型偏好：{', '.join(self.user_travel_info.spot_preference) or '无特殊偏好，可推荐热门且有特色的景点'}
        - 住宿需求：{', '.join(self.user_travel_info.hotel_preference) or '无特殊需求，推荐舒适且性价比高的住宿'}
        - 特殊需求：{', '.join(self.user_travel_info.special_needs) or '无特殊需求'}
        """

        # 推荐路线信息
        recommend_route = self.travel_route_list.routes[self.travel_route_list.recommend_route_index]
        route_info = f"""
        【推荐路线信息】
        - 路线类型：{recommend_route.route_type}
        - 总耗时：{recommend_route.total_time}
        - 总费用：{recommend_route.total_cost}
        - 途经城市：{', '.join(recommend_route.passing_areas)}
        """

        # 景点信息（详细列出，方便大模型选择）
        landmark_info = "【搜集到的景点信息】\n"
        for idx, landmark in enumerate(self.landmark_options, 1):
            landmark_info += f"{idx}. 名称：{landmark.name}，类型：{landmark.type}，简介：{landmark.intro[:100]}...，地址：{landmark.address}，热度：{landmark.hot}\n"

        # 美食信息（详细列出，方便大模型选择）
        food_info = "【搜集到的美食信息】\n"
        for idx, food in enumerate(self.food_options, 1):
            food_info += f"{idx}. 名称：{food.name}，类型：{food.type}，招牌菜：{food.recommend}，评分：{food.score}，地址：{food.address}\n"

        # 酒店信息（详细列出，方便大模型选择）
        hotel_info = "【搜集到的酒店信息】\n"
        for idx, hotel in enumerate(self.hotel_option_list.hotels, 1):
            hotel_info += f"{idx}. 名称：{hotel.name}，星级：{hotel.star}，评分：{hotel.score}，价格：{hotel.price}，地址：{hotel.address}\n"

        # 整合所有信息
        all_info = f"{user_info}\n{route_info}\n{landmark_info}\n{food_info}\n{hotel_info}"
        return f"现在需要你基于以下所有信息，为用户生成一份旅游推荐方案：\n{all_info}"

    def _generate_fallback_plan(self) -> str:
        """当LLM调用失败时生成的备用方案"""
        recommend_route = self.travel_route_list.routes[self.travel_route_list.recommend_route_index]
        recommend_hotel = self.hotel_option_list.hotels[self.hotel_option_list.recommend_hotel_index]
        
        plan = f"【旅游规划概要】\n"
        plan += f"出发地：{self.user_travel_info.departure_city} → 目的地：{self.user_travel_info.destination_city}\n"
        plan += f"日期：{self.user_travel_info.start_date} 至 {self.user_travel_info.end_date}\n\n"
        
        plan += f"【推荐路线】\n"
        plan += f"方式：{recommend_route.route_type}，耗时：{recommend_route.total_time}，费用：{recommend_route.total_cost}\n"
        plan += f"途经：{', '.join(recommend_route.passing_areas)}\n\n"
        
        plan += f"【推荐景点】\n"
        for lm in self.landmark_options[:3]:
            plan += f"- {lm.name}（{lm.type}）\n"
        
        plan += f"\n【推荐美食】\n"
        for food in self.food_options[:3]:
            plan += f"- {food.name}（{food.type}）：{food.recommend}\n"
        
        plan += f"\n【推荐酒店】\n"
        plan += f"- {recommend_hotel.name}：{recommend_hotel.star}，{recommend_hotel.price}，{recommend_hotel.address}\n"
        
        return plan
    
    

    

