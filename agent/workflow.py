from ..agent.chat_agent.agent import ChatAgent
from ..agent.chat_agent.key_point_extract import key_point_extract

def test():
    agent = ChatAgent()
    travel_dict = key_point_extract()
    travel_info = agent.get_travel_info(travel_dict)
    path = agent.get_path_info()
    hotel_info = agent.get_hotel_info(top_n=5)
    tourism_info = agent.get_tourism_info()
    food_info = agent.get_food_info()
    travel_plan = agent.generate_comprehensive_travel_plan()
    print("="*50, flush=True)
    print("📅 完整旅游规划", flush=True)
    print("="*50, flush=True)
    print(travel_plan, flush=True)


if __name__ == "__main__":
    test()