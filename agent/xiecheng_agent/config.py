from fake_useragent import UserAgent

# 初始化UserAgent对象
ua = UserAgent()

class Config:
    def __init__(self):
        self.request_url = "https://m.ctrip.com/restapi/soa2/34951/fetchHotelList"
        self.headers = {
            "User-Agent": ua.random,  # 自动生成随机User-Agent
            "sec-ch-ua-platform": "Windows",
            "Origin": "https://hotels.ctrip.com",
            "Content-Type": "application/json"
        }
        # 初始化请求体
        self.request_body = {
            "date": {
                "dateType": 1,
                "dateInfo": {
                    "checkInDate": "20250915",  # 入住日期
                    "checkOutDate": "20250917"   # 离店日期
                }
            },
            "destination": {
                "type": 1,
                "geo": {
                    "cityId": -1,          # 城市ID
                    "countryId": 1,        # 国家ID，1表示中国
                    "provinceId": 123      # 省份ID
                },
                "keyword": {
                    "word": ""             # 搜索关键词，可为空
                }
            },
            "extraFilter": {
                "childInfoItems": [],
                "ctripMainLandBDCoordinate": True,
                "sessionId": "",
                "extendableParams": {
                    "tripWalkDriveSwitch": "T"
                }
            },
            "filters": [
                {
                    "title": "6个月以内",
                    "value": "1",
                    "filterID": "88|1",
                    "type": "88"
                }
            ],
            "roomQuantity": 1,  # 房间数量
            "paging": {
                "pageIndex": 1,    # 页码
                "pageSize": 20,    # 每页数量
                "pageCode": "10650171192"
            },
            "hotelIdFilter": {
                "hotelAldyShown": []
            },
            "head": {
                "platform": "PC",
                "cver": "0",
                "cid": "",
                "bu": "HBU",
                "group": "ctrip",
                "aid": "",
                "sid": "",
                "ouid": "",
                "locale": "zh-CN",
                "timezone": "8",
                "currency": "CNY",
                "pageId": "10650171192",
                "vid": "",
                "guid": "",
                "isSSR": False,
                "extension": [
                    {"name": "cityId", "value": ""},  # 与destination.geo.cityId保持一致
                    {"name": "checkIn", "value": "2025-09-15"},  # 入住日期
                    {"name": "checkOut", "value": "2025-09-17"}, # 离店日期
                    {"name": "region", "value": "CN"}
                ]
            }
        }

    def set_location(self,city_id,province_id,country_id=1):
        """
        设置请求体中的城市、国家、省份ID
        :param city_id: 城市ID
        :param province_id: 省份ID
        :param country_id: 国家ID，默认1表示中国
        """
        self.request_body["destination"]["geo"]["cityId"] = city_id
        self.request_body["destination"]["geo"]["provinceId"] = province_id
        self.request_body["destination"]["geo"]["countryId"] = country_id
        # 同时更新head中的cityId
        for ext in self.request_body["head"]["extension"]:
            if ext["name"] == "cityId":
                ext["value"] = str(city_id)
            if ext["name"] == "provinceId":
                ext["value"] = str(province_id)
            if ext["name"] == "countryId":
                ext["value"] = str(country_id)


    def set_dates(self,check_in,check_out):
        """
        设置请求体中的入住和离店日期
        :param check_in: 入住日期，格式YYYYMMDD，如20250915
        :param check_out: 离店日期，格式YYYYMMDD，如20250917
        """
        self.request_body["date"]["dateInfo"]["checkInDate"] = check_in
        self.request_body["date"]["dateInfo"]["checkOutDate"] = check_out
        # 同时更新head中的checkIn和checkOut
        for ext in self.request_body["head"]["extension"]:
            if ext["name"] == "checkIn":
                ext["value"] = f"{check_in[:4]}-{check_in[4:6]}-{check_in[6:]}"
            if ext["name"] == "checkOut":
                ext["value"] = f"{check_out[:4]}-{check_out[4:6]}-{check_out[6:]}"