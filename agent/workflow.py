from .chat_agent.agent import ChatAgent
from .chat_agent.key_point_extract import key_point_extract

def test():
    agent = ChatAgent()
    travel_dict = key_point_extract()
    travel_info = agent.get_travel_info(travel_dict)
    path = agent.get_path_info()
    hotel_info = agent.get_hotel_info(top_n=5)
    tourism_info = agent.get_tourism_info()
    food_info = agent.get_food_info()
    travel_plan = agent.generate_comprehensive_travel_plan()
    # 5. 输出/返回规划结果（前端展示、对话回复等）
    print("="*50)
    print("📅 完整旅游规划")
    print("="*50)
    print(travel_plan)


if __name__ == "__main__":
    test()
