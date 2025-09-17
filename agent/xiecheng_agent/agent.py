import sys
import os
import json
import requests
import pandas as pd
from .config import Config

class XiechengAgent:
    def __init__(self):
        self.config = Config()
        self.headers = self.config.headers
        self.request_url = self.config.request_url
        # 获取当前脚本所在目录的绝对路径
        current_dir = os.path.dirname(os.path.abspath(__file__))
        # 拼接Excel文件的路径
        self.file_path = os.path.join(current_dir, "携程省市区ID对照表.xlsx")

    def get_city_id(self, city_name):
        try:
            # 读取Excel文件（假设已通过绝对路径正确定位文件）
            df = pd.read_excel(self.file_path)
            
            # 关键修改：用实际列名'城市名称'匹配，而非'城市'
            match = df[(df['城市名称'] == city_name)]
            
            if not match.empty:
                # 注意Excel中的省份ID列名是'省份ID'，城市ID列名是'城市ID'
                province_id = int(match.iloc[0]['省份ID'])  # 转换
                city_id = int(match.iloc[0]['城市ID'])        # 转换
                return city_id, province_id
            else:
                # 未找到匹配城市
                print(f"未找到城市 {city_name} 的ID信息")
                return -1, -1
                
        except Exception as e:
            print(f"获取城市ID时出错：{e}")
            return -1, -1
        
        
    
    def get_hotels(self, city_id:int, province_id:int, check_in_date, check_out_date, country_id=1, top_n=5):
        """
        获取指定城市的酒店信息（新增：提取酒店外观图URL、星级图URL）
        :param city_id: 城市ID
        :param province_id: 省份ID
        :param country_id: 国家ID,默认1表示中国
        :param check_in_date: 入住日期,格式YYYYMMDD
        :param check_out_date: 离店日期,格式YYYYMMDD
        :param top_n: 显示前N个结果
        :return: 包含外观图、星级图的酒店信息列表
        """
        # 设置城市
        self.config.set_location(city_id, province_id, country_id)
        # 设置日期
        self.config.set_dates(check_in_date, check_out_date)
        
        try:
            # 发送请求
            print("正在发送请求获取酒店信息...")
            response = requests.post(
                url=self.request_url,
                headers=self.headers,
                json=self.config.request_body,
                timeout=15
            )
            
            print(f"请求状态码: {response.status_code}")
            
            if response.status_code == 200:
                try:
                    hotel_data = response.json()
                    hotel_list = hotel_data.get("data", {}).get("hotelList", [])
                    print(f"获取到 {len(hotel_list)} 家酒店")
                    
                    if len(hotel_list) > 0:
                        parsed_hotels = []
                        for hotel in hotel_list:
                            hotel_info = hotel.get("hotelInfo", {})

                            # 1. 提取酒店名称
                            name = hotel_info.get("nameInfo", {}).get("name", "未知名称")
                            
                            # 2. 提取酒店地址
                            address = hotel_info.get("positionInfo", {}).get("address", "未知地址")
                            
                            # -------------------------- 新增：提取酒店外观图片（第一个URL） --------------------------
                            # 路径：hotelInfo -> hotelImages -> multiImgs（取第一个元素的url）
                            hotel_images = hotel_info.get("hotelImages", {})
                            multi_imgs = hotel_images.get("multiImgs", [])  # 图片列表
                            # 若有图片，取第一个作为外观图；无则设为"暂无"
                            appearance_img_url = multi_imgs[0].get("url", "暂无外观图") if multi_imgs else "暂无外观图"
                            
                            # -------------------------- 新增：提取星级图片URL + 星级等级 --------------------------
                            # 路径：hotelInfo -> hotelStar（star=星级，starIconUrl=星级图标URL）
                            hotel_star = hotel_info.get("hotelStar", {})
                            star_level = hotel_star.get("star", "未知星级")  # 如：4（表示4星）
                            star_icon_url = hotel_star.get("starIconUrl", "暂无星级图标")  # 星级图片链接
                            
                            # 3. 提取酒店评分
                            score = hotel_info.get("commentInfo", {}).get("commentScore", "暂无评分")
                            score_desc = hotel_info.get("commentInfo", {}).get("commentDescription", "")
                            full_score = f"{score} ({score_desc})" if score_desc else score
                            
                            # 4. 提取酒店价格（保留原逻辑）
                            price = "未知价格"
                            room_info_list = hotel.get("roomInfo", [])
                            if room_info_list:
                                # 优先从 ratePlanInfo 提取价格
                                rate_plan_info = room_info_list[0].get("ratePlanInfo", {})
                                if rate_plan_info:
                                    price = rate_plan_info.get("price", rate_plan_info.get("currentPrice", "未知价格"))
                                # 其次从 priceDetail 提取
                                if price == "未知价格":
                                    price_detail = room_info_list[0].get("priceDetail", {})
                                    price = price_detail.get("price", "未知价格")
                                # 最后从 extend 提取
                                if price == "未知价格":
                                    hotel_extend = hotel_info.get("extend", {})
                                    price = hotel_extend.get("priceInfo", {}).get("price", "未知价格")

                            # -------------------------- 组装最终数据（新增外观图、星级图字段） --------------------------
                            parsed = {
                                "name": name,
                                "address": address,
                                "score": full_score,
                                "price": price,
                                "star_level": f"{star_level}星" if str(star_level).isdigit() else star_level,  # 格式化星级（如"4星"）
                                "appearance_img_url": appearance_img_url,  # 酒店外观图URL
                                "star_icon_url": star_icon_url,          # 星级图标URL
                                "original_data": hotel  # 保留原始数据用于调试
                            }
                            parsed_hotels.append(parsed)
                        
                        # 按价格排序（保留原逻辑）
                        def get_price_value(hotel):
                            try:
                                price_str = str(hotel["price"]).replace("元", "").strip()
                                return float(price_str)
                            except:
                                return float('inf')  # 无法转换的价格放最后
                        
                        sorted_hotels = sorted(parsed_hotels, key=get_price_value)
                        
                        # 打印结果（新增外观图、星级信息展示）
                        print(f"\n按价格排序的前{min(top_n, len(sorted_hotels))}家酒店信息：")
                        print("-" * 150)  # 加宽分隔线
                        
                        for i, hotel in enumerate(sorted_hotels[:top_n], 1):
                            print(f"{i}. 酒店名称：{hotel['name']}")
                            print(f"   价格：{hotel['price']}元" if hotel['price'] != "未知价格" else f"   价格：{hotel['price']}")
                            print(f"   星级：{hotel['star_level']} | 星级图标URL：{hotel['star_icon_url']}")
                            print(f"   地址：{hotel['address']}")
                            print(f"   评分：{hotel['score']}")
                            print(f"   外观图URL：{hotel['appearance_img_url']}")  # 打印外观图链接
                            print("-" * 150)
                        
                        return sorted_hotels[:top_n]
                    else:
                        print("未获取到酒店信息")
                except json.JSONDecodeError:
                    print("响应不是有效的JSON格式")
                    print("响应内容:", response.text)
            else:
                print(f"请求失败，状态码：{response.status_code}")
                print("响应内容:", response.text)
                
        except Exception as e:
            print(f"请求过程中发生错误：{str(e)}")
        
        return None

if __name__ == "__main__":
    agent = XiechengAgent()
    # 调用时会返回包含外观图、星级图的酒店列表
    result = agent.get_hotels(
        city_id=5, 
        province_id=5, 
        check_in_date="20250920", 
        check_out_date="20250925"
    )
