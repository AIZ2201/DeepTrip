# coding=UTF-8
import sys
import time
from .scenicInfo import ScenicInfo
from .config import Config

# 确保标准输出使用UTF-8编码
sys.stdout.reconfigure(encoding='utf-8')

class Agent:
    def __init__(self, config=None):
        """
        初始化景点智能体
        :param config: 配置对象，如果为None则使用默认配置
        """
        if config is None:
            config = Config()
        self.config = config
        self.scenic_info = ScenicInfo(config)
        self.last_result = None  # 保存最后一次查询结果
        self.batch_results = {}  # 保存批量查询结果
    
    def search_scenic_spots(self, area="", page=1):
        """
        搜索景点信息 - 只使用area参数进行查询，page默认为1
        :param area: 地区（必填）
        :param page: 页码（默认1）
        :return: 景点信息结果
        """
        try:
            # 确保参数为字符串类型
            area = str(area) if area else ""
            
            # 验证area参数不为空
            if not area:
                return {"code": -1, "message": "地区参数不能为空"}
            
            print(f"正在查询 {area} 的景点信息...")
            # 只传递area和page参数，其他参数使用默认空字符串
            result = self.scenic_info.get_scenic_info(area=area, name="", type="", page=page)
            # 打印原始结果用于调试
            print(f"原始API响应: {result}")
            self.last_result = result  # 保存结果
            return result
        except Exception as e:
            return {"code": -1, "message": f"搜索失败: {str(e)}"}
    
    def batch_search_scenic_spots(self, area_list, page=1, delay=0.5, merge_results=False, sort_by_hot=False):
        """
        批量搜索多个地区的景点信息
        :param area_list: 地区列表
        :param page: 页码（默认1）
        :param delay: 每个查询之间的延迟时间（秒），防止请求过于频繁
        :param merge_results: 是否合并所有结果
        :param sort_by_hot: 是否按热度排序合并后的结果
        :return: 批量查询结果
        """
        if not isinstance(area_list, list) or len(area_list) == 0:
            return {"code": -1, "message": "地区列表不能为空"}
        
        print(f"开始批量查询 {len(area_list)} 个地区的景点信息...")
        
        # 清空之前的批量查询结果
        self.batch_results = {}
        
        # 合并结果容器
        merged_scenic_spots = []
        total_count = 0
        
        # 遍历地区列表进行查询
        for i, area in enumerate(area_list):
            try:
                print(f"[{i+1}/{len(area_list)}] 查询地区: {area}")
                
                # 调用单个查询方法
                result = self.search_scenic_spots(area, page)
                
                # 解析结果
                parsed_result = self._parse_scenic_result(result)
                
                # 保存结果
                self.batch_results[area] = parsed_result
                
                # 如果需要合并结果
                if merge_results and parsed_result.get("scenic_spots"):
                    # 添加地区标识
                    for spot in parsed_result["scenic_spots"]:
                        spot["source_area"] = area
                        merged_scenic_spots.append(spot)
                    total_count += parsed_result.get("total_count", 0)
                
                # 如果不是最后一个查询，添加延迟
                if i < len(area_list) - 1:
                    print(f"等待 {delay} 秒后继续下一个查询...")
                    time.sleep(delay)
                
            except Exception as e:
                print(f"查询 {area} 时出错: {str(e)}")
                self.batch_results[area] = {"code": -1, "message": str(e)}
        
        # 如果需要返回合并后的结果
        if merge_results:
            merged_result = {
                "total_count": total_count,
                "total_pages": 1,  # 批量查询默认只返回一页
                "current_page": 1,
                "status": "成功",
                "scenic_spots": merged_scenic_spots
            }
            
            # 如果需要按热度排序，这里移除了排序功能，因为新API没有热度字段
            
            return merged_result
        
        return self.batch_results
    
    def _parse_scenic_result(self, result):
        """
        解析景点信息结果
        根据新的API返回格式进行解析
        """
        if not result:
            return {"code": -1, "message": "返回结果为空"}
        
        # 检查响应状态
        resp_code = result.get("resp", {}).get("RespCode", "")
        resp_msg = result.get("resp", {}).get("RespMsg", "查询失败")
        
        if resp_code != "200":
            return {"code": int(resp_code) if resp_code.isdigit() else -1, "message": resp_msg}
        
        try:
            # 提取数据部分
            data = result.get("data", {})
            scenic_list = data.get("record", [])
            
            # 从data中获取总记录数和总页数
            total_count = int(data.get("totalcount", "0"))
            total_pages = int(data.get("totalpage", "1"))
            current_page = 1  # 可以从请求参数中获取或默认为1
            
            parsed_result = {
                "total_count": total_count,
                "total_pages": total_pages,
                "current_page": current_page,
                "status": "成功" if resp_code == "200" else "失败",
                "scenic_spots": []
            }
            
            # 遍历景点列表，提取所需字段
            for spot in scenic_list:
                parsed_spot = {
                    "name": spot.get("spot", ""),
                    "level": spot.get("grade", "无等级"),
                    "address": spot.get("addr", ""),
                    "intro": spot.get("type", ""),
                    "area": spot.get("addr", ""),  # 使用地址作为区域信息
                    "type": spot.get("type", "")
                }
                parsed_result["scenic_spots"].append(parsed_spot)
            
            return parsed_result
        except Exception as e:
            print(f"解析错误: {str(e)}")
            return {"code": -1, "message": f"解析失败: {str(e)}"}
    
    def print_beautiful_scenic_info(self, result):
        """
        美观打印景点信息
        """
        if not result:
            print("❌ 没有找到景点信息")
            return
        
        if "code" in result and result["code"] != 200 and "message" in result:
            print(f"❌ 查询失败: {result['message']}")
            return
        
        try:
            print(f"✅ 查询成功！共找到 {result.get('total_count', 0)} 个景点")
            print(f"📄 当前页码: {result.get('current_page', 1)} / {result.get('total_pages', 1)}")
            print(f"📊 状态: {result.get('status', '未知')}")
            print("=" * 50)
            
            for spot in result.get('scenic_spots', []):
                # 如果是合并结果，显示来源地区
                if 'source_area' in spot:
                    print(f"🌍  来源地区: {spot['source_area']}")
                
                print(f"🏞️  景点名称: {spot.get('name', '')}")
                print(f"⭐  景点等级: {spot.get('level', '无等级')}")
                print(f"📍  地址: {spot.get('address', '')}")
                print(f"🌍  地区: {spot.get('area', '')}")
                print(f"🏷️  类型: {spot.get('type', '')}")
                
                # 处理简介
                print(f"📝  简介: {spot.get('intro', '')}")
                
                # 新API中的其他信息
                if spot.get('visittime'):
                    print(f"⏱️  建议游览时间: {spot['visittime']}")
                if spot.get('opentime'):
                    print(f"🕒  开放时间: {spot['opentime']}")
                if spot.get('tel'):
                    print(f"📞  联系电话: {spot['tel']}")
                if spot.get('url'):
                    print(f"🔗  官方网站: {spot['url']}")
                if spot.get('lng') and spot.get('lat'):
                    print(f"🗺️  经纬度: {spot['lat']}, {spot['lng']}")
                
                print("-" * 50)
        except Exception as e:
            print(f"❌ 打印失败: {str(e)}")
    
    def sort_scenic_spots_by_hot(self, parsed_result):
        """
        注意：新的API没有热度字段，此函数仅保留兼容性
        """
        if not parsed_result or not parsed_result.get("scenic_spots"):
            return parsed_result
        
        print("注意：新的API返回数据中没有热度字段，无法按热度排序")
        return parsed_result

# 主函数示例
if __name__ == "__main__":
    try:
        config = Config()
        agent = Agent(config)
        '''
        # 设置查询参数 - 地理位置列表
        area_list = [
            '北京·东城区', '北京·朝阳区', '北京·大兴区', '廊坊市·广阳区',
            '天津·武清区', '天津·西青区', '沧州市·黄骅市', '滨州市·无棣县',
            '滨州市·沾化区', '滨州市·博兴县', '东营市·广饶县', '潍坊市·青州市',
            '潍坊市·临朐县', '临沂市·沂水县', '日照市·莒县', '临沂市·莒南县',
            '连云港市·赣榆区', '连云港市·灌云县', '盐城市·响水县', '南通市·海安市',
            '苏州市·常熟市', '苏州市·昆山市', '上海·嘉定区', '上海·普陀区',
            '上海·静安区', '上海·黄浦区'
        ]
        '''
        area_list = ['济南市']
        # 批量搜索景点 - 设置延迟防止请求过于频繁，合并结果
        merged_result = agent.batch_search_scenic_spots(
            area_list=area_list, 
            page=1, 
            delay=1, 
            merge_results=True
        )
        
        # 美观打印合并后的结果
        agent.print_beautiful_scenic_info(merged_result)
        
        print("\n📊 批量查询完成！")
            
    except Exception as e:
        print(f"❌ 程序错误: {str(e)}")