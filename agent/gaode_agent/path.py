import requests
import json
from .config import Config
from .location import Location

class Path:
    def __init__(self, config: Config):
        self.api_key = config.api_key
        self.url = config.path_url  # 确保是高德驾车路径API：https://restapi.amap.com/v3/direction/driving
        self.location = Location(config)

    def get_path(self, origin: str, destination: str):
        params = {
            "key": self.api_key,
            "origin": origin,
            "destination": destination,
            # 重点：确保show_fields字段拼写正确、逗号分隔无空格
            "show_fields": "cost,cities"
        }

        try:
            response = requests.get(self.url, params=params)
            response.raise_for_status()
            result = response.json()
            
            if result.get("status") == "1":
                print(f"✅ 从 '{origin}' 到 '{destination}' 的路径请求成功")
                return result
            else:
                print(f"❌ 路径请求失败：{result.get('info')}")
                return None

        except requests.exceptions.RequestException as e:
            print(f"❌ 路径请求异常：{e}")
            return None