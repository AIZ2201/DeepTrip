import os
import sys

class Config:
    def __init__(self):
        # 高德地图API配置
        self.api_key = '21dea60b3a2e5d79e86dff7cedeee222'  # 请替换为你的高德地图API密钥
        
        # 餐饮搜索相关URL
        self.food_url = 'https://restapi.amap.com/v5/place/text?parameters'
        
        # 确保UTF-8编码
        self.ensure_utf8()
    
    def ensure_utf8(self):
        # 确保系统环境使用UTF-8编码
        if sys.version_info[0] == 3:
            # Python 3 默认就是UTF-8，不需要特别处理
            pass
        else:
            # Python 2 的处理方式
            reload(sys)
            sys.setdefaultencoding('utf-8')