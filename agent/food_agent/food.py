# coding=UTF-8
import requests
import sys

# 确保标准输出使用UTF-8编码
sys.stdout.reconfigure(encoding='utf-8')

class Food:
    def __init__(self, config):
        self.api_key = config.api_key
        self.food_url = config.food_url
    
    def search_food_by_keyword(self, keyword, city):
        """
        根据关键词搜索餐饮信息
        :param keyword: 搜索关键词，如"川菜"、"火锅"等
        :param city: 城市名称，如"北京"、"上海"等
        :param page: 页码，默认为1
        :param page_size: 每页结果数量，默认为20
        :return: 餐饮信息搜索结果
        """
        try:
            # POI类型：餐饮服务（大类）
            poi_type = "050000"
            
            params = {
                "key": self.api_key,
                "keywords": keyword,
                "types": poi_type,
                "region": city,
                "show_fields": "business"
            }
            
            response = requests.get(self.food_url, params=params)
            response.raise_for_status()
            
            result = response.json()
            
            print(result)

            if result.get("status") == "1":
                pois = result.get("pois", [])
                total_count = int(result.get("count", "0"))
                
                print(f"在{keyword}搜索美食，共找到{total_count}家餐饮场所")
                return result
            else:
                print(f"餐饮搜索失败: {result.get('info', '未知错误')}")
                return None
                
        except requests.exceptions.RequestException as e:
            print(f"餐饮搜索请求异常: {str(e)}")
            return None