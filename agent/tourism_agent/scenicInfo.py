# coding=UTF-8
import requests
import sys
import time

# 确保标准输出使用UTF-8编码
sys.stdout.reconfigure(encoding='utf-8')

class ScenicInfo:
    def __init__(self, config):
        self.appcode = config.appcode
        self.host = config.host
        self.path = config.path
        self.method = config.method
        self.timeout = config.timeout
        self.max_retries = config.max_retries
        self.headers = {
            "Authorization": f"APPCODE {self.appcode}"
        }
        
    def get_scenic_info(self, area="", name="", type="", page=1):
        """
        获取景点信息
        :param area: 地区
        :param name: 景点名称
        :param type: 景点类型
        :param page: 页码
        :return: 景点信息JSON
        """
        retries = 0
        while retries < self.max_retries:
            try:
                # 构建完整的URL（不包含查询参数）
                url = f"{self.host}{self.path}"
                
                # 使用params参数让requests自动处理URL编码
                params = {
                    "city": area,
                    "page": page
                }
                
                # 发送请求，让requests自动处理URL编码
                response = requests.get(url, headers=self.headers, params=params, timeout=self.timeout)

                # 确保响应内容使用UTF-8编码解析
                response.encoding = 'utf-8'
                
                if response.status_code == 200:
                    return response.json()
                else:
                    # 对于特定错误码尝试重试
                    if response.status_code in [500, 502, 503, 504] and retries < self.max_retries - 1:
                        retries += 1
                        print(f"请求失败，正在重试 ({retries}/{self.max_retries})...")
                        time.sleep(1)  # 等待1秒后重试
                        continue
                    return self._handle_error(response)
            except requests.exceptions.Timeout:
                retries += 1
                if retries < self.max_retries:
                    print(f"请求超时，正在重试 ({retries}/{self.max_retries})...")
                    time.sleep(1)
                    continue
                return {"code": -1, "message": f"请求超时: 已重试{self.max_retries}次"}
            except Exception as e:
                return {"code": -1, "message": f"请求异常: {str(e)}"}
        
    def _handle_error(self, response):
        """处理API返回的错误"""
        try:
            httpStatusCode = response.status_code
            httpReason = response.headers.get('X-Ca-Error-Message', '')
            
            # 根据API文档中的错误码处理
            if httpStatusCode == 400:
                if httpReason == 'Invalid Param Location':
                    return {"code": 400, "message": "参数错误"}
                elif httpReason == 'Invalid AppCode':
                    return {"code": 400, "message": "AppCode错误"}
                elif httpReason == 'Invalid Url':
                    return {"code": 400, "message": "请求的 Method、Path 或者环境错误"}
            elif httpStatusCode == 403:
                if httpReason == 'Unauthorized':
                    return {"code": 403, "message": "服务未被授权（或URL和Path不正确）"}
                elif httpReason == 'Quota Exhausted':
                    return {"code": 403, "message": "套餐包次数用完"}
                elif httpReason == 'Api Market Subscription quota exhausted':
                    return {"code": 403, "message": "套餐包次数用完，请续购套餐"}
            elif httpStatusCode == 500:
                return {"code": 500, "message": "API网关错误"}
            
            # 其他未预期的错误
            return {"code": httpStatusCode, "message": f"参数名错误或其他错误: {httpReason}"}
        except Exception as e:
            return {"code": -1, "message": f"错误处理异常: {str(e)}"}
    
    def get_scenic_details(self, scenic_id):
        """
        获取单个景点的详细信息
        :param scenic_id: 景点ID
        :return: 景点详细信息
        """
        try:
            # 注意：这里假设API支持通过ID查询景点详情
            # 实际实现需要根据API文档调整参数
            url = f"{self.host}{self.path}"
            params = {
                "id": scenic_id
            }
            
            response = requests.get(url, headers=self.headers, params=params, timeout=self.timeout)
            response.encoding = 'utf-8'
            
            if response.status_code == 200:
                return response.json()
            else:
                return self._handle_error(response)
        except Exception as e:
            return {"code": -1, "message": f"获取景点详情失败: {str(e)}"}
    
    def search_by_location(self, lat, lng, radius=5000):
        """
        根据经纬度搜索附近的景点
        :param lat: 纬度
        :param lng: 经度
        :param radius: 搜索半径(米)
        :return: 附近景点列表
        """
        try:
            # 注意：这里假设API支持根据经纬度搜索
            # 实际实现需要根据API文档调整参数
            url = f"{self.host}{self.path}"
            params = {
                "location": f"{lat},{lng}",
                "radius": radius
            }
            
            response = requests.get(url, headers=self.headers, params=params, timeout=self.timeout)
            response.encoding = 'utf-8'
            
            if response.status_code == 200:
                return response.json()
            else:
                return self._handle_error(response)
        except Exception as e:
            return {"code": -1, "message": f"搜索附近景点失败: {str(e)}"}