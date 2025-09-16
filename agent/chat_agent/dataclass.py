from dataclasses import dataclass
from typing import List, Optional

#声明一个数据类来存储用户的旅游偏好
@dataclass
class UserTravelPreference:
    """用户旅游偏好（从你的提取工具中获取的结果）"""
    departure_city: str  # 出发地（如“南京”）
    destination_city: str  # 目的地（如“北京”）
    start_date: str  # 出发日期（YYYYMMDD，如“20241001”）
    end_date: str  # 结束日期（YYYYMMDD，如“20241003”）
    budget: str  # 预算（如“3000元”）
    spot_preference: List[str]  # 景点偏好（如["历史遗迹"]）
    hotel_preference: List[str]  # 住宿偏好（如["靠近地铁"]）
    special_needs: List[str]  # 特殊需求（如["未明确"]）


@dataclass
class TravelRoute:
    """
    旅游路线数据类（适配你提供的路线格式：总耗时/收费/途经区县等）
    """
    total_time: str  # 总耗时（如“10小时31分钟”）
    total_cost: str  # 总收费（如“438.00元”，保留原始格式）
    toll_mileage: str  # 收费里程（如“939.7公里”）
    traffic_light_count: int  # 红绿灯数量（如31个）
    passing_areas: List[str]  # 途经城市/区县（如['南京市-玄武区', '滁州市-来安县']）
    route_type: Optional[str] = "自驾"  # 路线类型（默认“自驾”，可扩展“高铁”“飞机”）
    start_point: Optional[str] = None  # 路线起点（如“南京市”，从用户偏好中同步）
    end_point: Optional[str] = None  # 路线终点（如“北京市”，从用户偏好中同步）

@dataclass
class TravelRouteList:
    '''
    多条路线的容器管理
    '''
    routes : List[TravelRoute]
    recommend_route_index : int #推荐路线的索引，从0开始
    start_city : str #起点城市 统一
    end_city : str #终点城市 统一

#酒店信息
@dataclass
class HotelOption:
    name: str  # 对应字典的"name"
    address: str  # 对应字典的"address"
    star: str  # 对应字典的"star_level"（如"4星"）
    score: str  # 对应字典的"score"（如"4.8 (超棒)"）
    hotel_image_url: str  # 对应字典的"appearance_img_url"
    star_image_url: str  # 对应字典的"star_icon_url"
    price: str = "未知价格"  # 对应字典的"price"（默认值）
    data_source: Optional[str] = "携程API"  # 固定值

@dataclass
class HotelOptionList:
    hotels: List[HotelOption]  # HotelOption实例列表
    sort_type: str  # 排序方式（你的代码中是"按价格升序"）
    total_count: int  # 实际返回的酒店数量
    destination_city: str  # 酒店所在城市（从用户偏好获取）
    check_in_date: str  # 入住日期（YYYYMMDD）
    check_out_date: str  # 离店日期（YYYYMMDD）
    recommend_hotel_index: Optional[int] = 0  # 推荐酒店索引

#景点信息
@dataclass
class LandmarkOption:
    """
    景点信息
    """
    area: str #景点区域(如"南京市-玄武区")
    name: str #景点名称(如"玄武区历史遗址")
    level:str #景点等级(如"4A")
    address: str #景点地址(如"南京市-玄武区-玄武区历史遗址")
    type: str #景点类型(如"历史遗址")
    intro: str #景点介绍(如"玄武区历史遗址是南京历史上的一个重要景点")
    hot:str #景点热度

@dataclass
class FoodOption:
    """
    美食饭店信息
    """
    name: str #美食饭店名称
    score:str #美食饭店评分
    address: str #美食饭店地址
    type: str #美食饭店类型
    area: str #美食饭店区域
    tel: str #美食联系电话
    recommend: str #美食推荐