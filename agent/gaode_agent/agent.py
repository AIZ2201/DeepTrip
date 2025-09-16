from .config import Config
from .path import Path
from .location import Location
from ..chat_agent.key_point_extract import key_point_extract

class GaodeAgent:
    def __init__(self):
        self.config = Config()
        self.location = Location(self.config)
        self.path = Path(self.config)

    def get_path(self, address1: str, address2: str):
        loc1 = self.location.get_location(address1)
        loc2 = self.location.get_location(address2)
        if loc1 and loc2:
            if loc1.get("status") == "1" and loc2.get("status") == "1":
                geocodes1 = loc1.get("geocodes", [])
                geocodes2 = loc2.get("geocodes", [])
                if geocodes1 and geocodes2:
                    location1 = geocodes1[0].get("location")
                    location2 = geocodes2[0].get("location")
                    path = self.path.get_path(location1, location2)
                    return path
                else:
                    print("未找到地址的经纬度信息。")
                    return None
            else:
                print("获取地址经纬度失败。")
                return None
        else:
            print("获取地址经纬度时发生错误。")
            return None


def parse_gaode_result(result):
    """
    解析高德API返回的result，提取所有路线方案的信息
    :param result: 高德API返回的完整字典
    :return: 所有路线的结构化结果列表
    """
    all_routes = []
    routes = result.get("route", {})
    # 获取所有路径方案（paths数组）
    all_paths = routes.get("paths", [])
    
    if not all_paths:
        return [{"error": "无有效路径数据"}]
    
    # 遍历每条路线并解析
    for route_idx, path in enumerate(all_paths, 1):  # 从1开始编号
        # 提取当前路线的基础信息
        cost = path.get("cost", {})
        total_duration = cost.get("duration", "0")  # 总耗时（秒）
        total_tolls = cost.get("tolls", "0")        # 总收费（元）
        toll_distance = cost.get("toll_distance", "0")  # 收费里程（米）
        traffic_lights = cost.get("traffic_lights", "0")  # 红绿灯数量
        
        # 格式化耗时
        hour = int(total_duration) // 3600
        minute = (int(total_duration) % 3600) // 60
        duration_str = f"{hour}小时{minute}分钟"
        
        # 格式化收费里程
        toll_km = f"{int(toll_distance) / 1000:.1f}公里" if toll_distance != "0" else "0公里"
        
        # 提取当前路线的途经城市（按实际顺序去重）
        passed_cities = []
        steps = path.get("steps", [])
        for step in steps:
            cities = step.get("cities", [])
            for city_info in cities:
                city_name = city_info.get("city", "")
                district = city_info.get("districts", [{}])[0].get("name", "")
                full_city = f"{city_name}-{district}" if district else city_name
                if full_city and full_city not in passed_cities:
                    passed_cities.append(full_city)
        
        # 存储当前路线的信息（添加路线编号）
        all_routes.append({
            "路线编号": route_idx,
            "总耗时": duration_str,
            "总收费": f"{float(total_tolls):.2f}元" if total_tolls != "0" else "0元",
            "收费里程": toll_km,
            "红绿灯数量": f"{traffic_lights}个",
            "途经城市/区县": passed_cities if passed_cities else "无"
        })
    
    return all_routes

'''
if __name__ == "__main__":
    config = Config()
    agent = Agent(config)
    travel_dict = key_point_extract()
    address1 = travel_dict["出发点"] 
    address2 = travel_dict["目的地"]
    if address1 is not None and address2 is not None:
        path_info = agent.get_path(address1, address2)
    if path_info:
        # 解析所有路线
        all_routes = parse_gaode_result(path_info)
        # 打印每条路线
        for route in all_routes:
            print(f"\n===== 路线{route['路线编号']} =====")
            for key, value in route.items():
                if key != "路线编号":  # 已在标题中显示编号，避免重复
                    print(f"{key}: {value}")

'''