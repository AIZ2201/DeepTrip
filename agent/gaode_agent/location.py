import requests
import json
from .config import Config

class Location:
    def __init__(self,config: Config):
        self.api_key = config.api_key
        self.url = config.location_url

    def get_location(self,address:str):
        #定义请求参数
        params = {
            "key":self.api_key,
            "address":address,
        }
        #发送请求
        try:
                # 发送GET请求
            response = requests.get(self.url, params=params)
            # 检查请求是否成功
            response.raise_for_status()
            
            # 解析JSON响应
            result = response.json()
            
            
            # 检查返回状态
            if result.get("status") == "1":
                # 提取经纬度信息
                geocodes = result.get("geocodes", [])
                if geocodes:
                    location = geocodes[0].get("location")
                    print(f"地址 '{address}' 的经纬度：{location}")
            else:
                print(f"\n请求失败：{result.get('info')}")
                
            return result
            
        except requests.exceptions.RequestException as e:
            print(f"请求发生错误：{e}")
            return None