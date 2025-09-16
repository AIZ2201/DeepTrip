# coding=UTF-8
import sys
import time
from .food import Food
from .config import Config

# 确保标准输出使用UTF-8编码
sys.stdout.reconfigure(encoding='utf-8')

class Agent:
    def __init__(self, config=None):
        """
        初始化餐饮智能体
        :param config: 配置对象，如果为None则使用默认配置
        """
        if config is None:
            config = Config()
        self.config = config
        self.food = Food(config)
        self.last_result = None  # 保存最后一次查询结果
    
    def search_food_by_keyword(self, keyword, city):
        """
        根据关键词搜索餐饮信息
        :param keyword: 搜索关键词
        :param city: 城市名称
        :param page: 页码
        :param page_size: 每页结果数量
        :return: 餐饮信息结果
        """
        try:
            if not keyword or not city:
                return {"code": -1, "message": "关键词和城市不能为空"}
            
            print(f"正在{city}搜索 '{keyword}' 相关的美食...")
            result = self.food.search_food_by_keyword(keyword, city)
            self.last_result = result
            return result
        except Exception as e:
            return {"code": -1, "message": f"搜索失败: {str(e)}"}
    
    def batch_search_food_by_keyword(self, cities, keyword="美食", delay=0.5):
        """
        批量搜索多个城市的餐饮信息
        :param cities: 城市列表
        :param keyword: 搜索关键词，默认为"美食"
        :param delay: 两次请求之间的延迟时间（秒），默认0.5秒
        :return: 合并后的餐饮信息结果
        """
        if not cities or not isinstance(cities, list):
            return {"code": -1, "message": "城市列表不能为空且必须是列表类型"}
        
        print(f"开始批量查询 {len(cities)} 个城市的'{keyword}'信息...")
        
        # 创建一个用于存储所有城市结果的字典
        merged_result = {
            "status": "成功",
            "total_count": 0,
            "food_list": []
        }
        
        for i, city in enumerate(cities):
            try:
                # 搜索当前城市的美食
                result = self.search_food_by_keyword(keyword, city)
                
                # 解析搜索结果
                parsed_result = self.parse_food_result(result)
                
                # 检查解析结果是否成功
                if "code" in parsed_result and parsed_result["code"] == -1:
                    print(f"❌ 城市 '{city}' 查询失败: {parsed_result.get('message', '未知错误')}")
                    continue
                
                # 合并结果
                if "food_list" in parsed_result:
                    for food in parsed_result["food_list"]:
                        # 添加城市标识
                        food["batch_city"] = city
                        merged_result["food_list"].append(food)
                    
                    # 更新总数量
                    merged_result["total_count"] += parsed_result.get("total_count", 0)
                    
                    print(f"✅ 城市 '{city}' 查询成功，找到 {len(parsed_result['food_list'])} 家餐饮场所")
                
                # 如果不是最后一个城市，添加延迟
                if i < len(cities) - 1 and delay > 0:
                    print(f"等待 {delay} 秒后继续下一个城市查询...")
                    time.sleep(delay)
                    
            except Exception as e:
                print(f"❌ 城市 '{city}' 查询异常: {str(e)}")
                continue
        
        print(f"✅ 批量查询完成！总共找到 {merged_result['total_count']} 家餐饮场所")
        return merged_result
    
    def parse_food_result(self, result):
        """
        解析餐饮信息结果
        :param result: API返回的原始结果
        :return: 解析后的结构化结果
        """
        if not result:
            return {"code": -1, "message": "返回结果为空"}
        
        # 检查状态码
        status = result.get("status", "0")
        if status != "1":
            return {"code": -1, "message": result.get("info", "查询失败")}
        
        try:
            pois = result.get("pois", [])
            total_count = int(result.get("count", "0"))
            
            parsed_result = {
                "total_count": total_count,
                "status": "成功" if status == "1" else "失败",
                "food_list": []
            }
            
            for poi in pois:
                # 提取餐饮场所信息
                parsed_poi = {
                    "name": poi.get("name", ""), # 名称
                    "address": poi.get("address", ""), # 地址
                    "type": poi.get("type", ""), # 类型
                    "area": poi.get("adname", ""), # 区域
                    "score": float(poi.get("business", {}).get("rating", "0")) if poi.get("business") else 0.0, # 评分
                    "recommend": poi.get("business", {}).get("tag", "").split(",") if poi.get("business") else [],# 推荐菜品
                    "tel": poi.get("business", {}).get("tel", "").split(";") if poi.get("business") else [],# 电话
                }
                
                parsed_result["food_list"].append(parsed_poi)
            
            return parsed_result
        except Exception as e:
            return {"code": -1, "message": f"解析失败: {str(e)}"}
    
    def print_beautiful_food_info(self, result):
        """
        美观打印餐饮信息
        :param result: 解析后的餐饮信息结果
        """
        if not result:
            print("❌ 没有找到餐饮信息")
            return
        
        if "code" in result and result["code"] != 200 and "message" in result:
            print(f"❌ 查询失败: {result['message']}")
            return
        
        try:
            print(f"✅ 查询成功！共找到 {result.get('total_count', 0)} 家餐饮场所")
            print("=" * 60)
            
            for food in result.get('food_list', []):
                # 如果是批量查询结果，显示城市来源
                if "batch_city" in food:
                    print(f"🏙️  城市: {food['batch_city']}")
                    
                print(f"🍽️  餐厅名称: {food.get('name', '')}")
                
                # 显示评分和人均消费
                rating = food.get('rating', 0.0)
                cost = food.get('cost', 0.0)
                if rating > 0 or cost > 0:
                    rating_str = f"⭐  评分: {rating}" if rating > 0 else ""
                    cost_str = f"💰  人均: ¥{cost}" if cost > 0 else ""
                    print(f"{rating_str} {cost_str}")
                
                # 显示地址
                print(f"📍  地址: {food.get('address', '')}")
                
                # 显示类型和区域
                type_info = food.get('type', '')
                if type_info:
                    print(f"🏷️  类型: {type_info}")
                    
                city = food.get('cityname', '')
                district = food.get('adname', '')
                business_area = food.get('business_area', '')
                if city and district:
                    area_info = f"{city}{district}"
                    if business_area:
                        area_info += f" ({business_area})"
                    print(f"🌍  区域: {area_info}")
                    
                # 显示电话（如果有）
                tel = food.get('tel', '')
                if tel:
                    print(f"📞  电话: {tel}")
                
                # 显示营业时间（如果有）
                opentime_today = food.get('opentime_today', '')
                if opentime_today:
                    print(f"⏰  今日营业时间: {opentime_today}")
                
                # 显示标签（如果有）
                tags = food.get('tags', [])
                if tags and tags != ['']:
                    # 筛选掉空标签
                    valid_tags = [tag for tag in tags if tag.strip()]
                    if valid_tags:
                        print(f"🏷️  推荐菜品: {', '.join(valid_tags)}")
                
                print("-" * 60)
                
        except Exception as e:
            print(f"❌ 打印失败: {str(e)}")
    
    def sort_food_by_rating(self, parsed_result):
        """
        按评分对餐饮场所进行排序
        :param parsed_result: 解析后的餐饮结果
        :return: 按评分排序后的结果
        """
        if not parsed_result or not parsed_result.get("food_list"):
            return parsed_result
        
        try:
            # 按评分降序排序
            parsed_result["food_list"].sort(key=lambda x: x.get("rating", 0), reverse=True)
            return parsed_result
        except Exception as e:
            print(f"排序失败: {str(e)}")
            return parsed_result

# 添加主函数示例
if __name__ == "__main__":
    # 初始化餐饮智能体
    agent = Agent()
    
    # 示例1: 单城市搜索
    # 搜索北京的火锅
    # result = agent.search_food_by_keyword("火锅", "北京")
    # 
    # # 解析结果
    # parsed_result = agent.parse_food_result(result)
    # 
    # # 按评分排序
    # sorted_result = agent.sort_food_by_rating(parsed_result)
    # 
    # # 美观打印结果
    # agent.print_beautiful_food_info(sorted_result)
    
    # 示例2: 批量城市搜索
    # 定义要搜索的城市列表
    cities = ["北京", "上海", "广州", "深圳"]
    
    # 批量搜索美食
    batch_result = agent.batch_search_food_by_keyword(cities, keyword="美食", delay=0.5)
    
    # 按评分排序
    if "food_list" in batch_result:
        sorted_result = agent.sort_food_by_rating(batch_result)
        
        # 美观打印结果
        # agent.print_beautiful_food_info(sorted_result)
        print(sorted_result)