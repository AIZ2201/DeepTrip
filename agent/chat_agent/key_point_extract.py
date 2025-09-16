import json
from openai import OpenAI

# 初始化OpenAI客户端（复用原有配置）
def get_response(messages):
    client = OpenAI(
        api_key="sk-31PqbF5zvpyDAbAYB1XrIu6d5eZpdjx3PyvHzM6Vab8RdrGS",
        base_url="https://api.chatanywhere.tech/v1",
    )
    completion = client.chat.completions.create(
        model="gpt-4o-2024-08-06",
        messages=messages,
        temperature=0.3,  # 低随机性，确保追问逻辑连贯
        max_tokens=1000,
        top_p=1,
        frequency_penalty=0.2,
        presence_penalty=0.2
    )
    return completion

# -------------------------- 核心1：优化System Prompt --------------------------
# 1. 规范“无需求”表述（禁止["无"]，统一用["未明确"]）
# 2. 强化城市名提取逻辑（避免省份残留）
# 3. 明确追问语气要求（更自然）
system_prompt = '''
你是一个贴心的旅游计划整理助手，需要帮用户收集旅游关键信息并整理成结构化字典，核心要做3件事：

### 1. 先判断信息缺什么
每次用户说完后，先检查这7个关键信息是否完整（缺了才问）：
- 出发点：必须是**纯城市名**（如“十堰”“武汉”，绝对不能包含省份/区域名如“湖北十堰”）
- 目的地：必须是**纯城市名**（如“武汉”“北京”，绝对不能包含省份/区域名如“湖北武汉”）
- 行程时间：要明确“入住日期+离店日期”（格式统一成YYYYMMDD，比如20251001）
- 经费预算：得有金额+单位（比如“3000元”“600元/天”）
- 景点类型偏好：具体类型（比如“爬山”“逛古镇”“看海”，别说“好玩就行”）
- 住宿需求：具体要求（如“要近地铁”“带早餐”“民宿优先”），用户说“没要求”“随便”则记为["未明确"]（禁止用["无"]）
- 特殊需求：明确约束（如“带2岁宝宝”“要无障碍设施”），用户说“没有”则记为["未明确"]（禁止用["无"]）

### 2. 再自然地追问
- 按“重要程度”问：先问最关键的（先问“去哪”→再问“什么时候去”→最后问“住什么要求/特殊需求”）
- 每次只问1个问题，别一次抛多个（避免用户信息过载）
- 语气像朋友聊天：比如用户说“想出去玩”，可以说“打算去哪个城市呀？比如青岛、成都这种具体的~”；用户说“从湖北十堰出发”，要确认“你是从十堰出发对吗？”
- 如果用户说“还没定”“不知道”，对应字段直接记为“未明确”，不用反复追问

### 3. 最后整理成字典
- 所有信息都齐了之后，**只输出1个Python字典**，别加任何多余话（比如“好的，整理好了”“这是你的计划”）
- 字典键名必须固定：["出发点","目的地","行程时间","经费预算","景点类型偏好","住宿需求","特殊需求"]
- 注意格式：
  - “出发点”和“目的地”只能是纯城市名，不包含任何省份、区域或具体地点（如“南京南站”→“南京”），出发地和目的地必须得有，不能为空
  - “行程时间”是子字典，必须包含“入住日期”“离店日期”两个键（格式YYYYMMDD）
  - “景点类型偏好”“住宿需求”“特殊需求”是列表类型（元素不重复，比如["古镇","看海"]，不能是“古镇、看海”）
  - 禁止出现任何格式错误（如单引号、遗漏逗号、键名写错）

注意：每次用户输入后，你都要先判断信息是否齐全，缺啥问啥，直到所有信息都收集齐了，才输出最终字典，别提前输出。
以及出发地，目的地以及行程时间都不能为空，必须都有，如果你没有提取到，可以重复询问。
如果目的地用户给出的是省份，可以询问用户具体到市。

举个例子：
用户输入：“我从湖北十堰出发去湖北武汉玩，十月二十号到二十三号，预算3000元，喜欢网红景点，住经济型酒店，没其他特殊要求。”
→ 输出字典：{
    "出发点": "十堰",
    "目的地": "武汉",
    "行程时间": {"入住日期":"20251020","离店日期":"20251023"},
    "经费预算":"3000元",
    "景点类型偏好":["网红景点"],
    "住宿需求":["经济型酒店"],
    "特殊需求":["未明确"]
  }
'''

# 初始化对话历史（包含系统指令）
messages = [{"role": "system", "content": system_prompt}]

# -------------------------- 核心2：优化交互循环 --------------------------
def extract_travel_preference():
    print("欢迎使用旅游偏好提取助手！请描述你的旅游计划，我会帮你整理（输入'退出'结束）\n")
    final_dict = None  # 新增：存储最终字典，避免退出时丢失结果
    while True:
        # 1. 获取用户输入
        user_input = input("你：").strip()
        if user_input.lower() in ["退出", "q", "quit"]:
            print("助手：已结束交互，感谢使用！")
            return final_dict  # 退出时返回最终字典（而非None）
        
        # 2. 将用户输入加入对话历史
        messages.append({"role": "user", "content": user_input})
        
        # 3. 调用LLM：判断是否需要追问，或直接输出字典
        try:
            response = get_response(messages)
            assistant_content = response.choices[0].message.content
            messages.append({"role": "assistant", "content": assistant_content})
            
            # 4. 优化字典判断逻辑：避免因键值对数量误判，改用“核心键+格式特征”判断
            is_final_dict = (
                "{" in assistant_content and "}" in assistant_content  # 包含字典符号
                and all(key in assistant_content for key in ["出发点", "目的地", "行程时间"])  # 包含核心键
                and "入住日期" in assistant_content and "离店日期" in assistant_content  # 行程时间子字典完整
            )
            
            if is_final_dict:
                # 处理字典格式：统一双引号、剔除多余字符
                dict_start = assistant_content.find("{")
                dict_end = assistant_content.rfind("}") + 1
                dict_str = assistant_content[dict_start:dict_end].replace("'", "\"").replace("\\", "")
                travel_dict = json.loads(dict_str)
                
                # 兜底1：确保出发地/目的地是纯城市名（剔除省份前缀）
                def clean_city(name):
                    provinces = ["河北","山西","辽宁","吉林","黑龙江","江苏","浙江","安徽","福建","江西","山东","河南","湖北","湖南","广东","海南","四川","贵州","云南","陕西","甘肃","青海","台湾","内蒙古","广西","宁夏","新疆","西藏","香港","澳门"]
                    for p in provinces:
                        if name.startswith(p):
                            return name.replace(p, "").strip()
                    return name
                travel_dict["出发点"] = clean_city(travel_dict["出发点"])
                travel_dict["目的地"] = clean_city(travel_dict["目的地"])
                
                # 兜底2：规范“未明确”字段（避免LLM仍输出["无"]）
                for key in ["住宿需求", "特殊需求"]:
                    if travel_dict.get(key) == ["无"]:
                        travel_dict[key] = ["未明确"]
                
                # 格式化输出结果
                print("\n助手：已获取你的完整旅游偏好，整理如下：")
                print(json.dumps(travel_dict, ensure_ascii=False, indent=2))
                print("\n✅ 可直接使用该字典对接后续服务（如酒店查询、行程规划）")
                
                # 存储最终字典，便于后续打印总结
                final_dict = travel_dict
                return final_dict  # 返回字典，结束交互循环
            
            else:
                # 输出追问话术，继续循环
                print(f"助手：{assistant_content}\n")
        
        except json.JSONDecodeError:
            # 若字典转换失败，视为追问（可能LLM格式有误）
            print(f"助手：{assistant_content}\n")
        except Exception as e:
            # 捕获其他错误，友好提示用户
            error_msg = str(e)[:30]  # 截取短错误信息，避免输出过长
            print(f"助手：获取信息时出现小问题，请再补充说明一下～（错误：{error_msg}...）\n")

# -------------------------- 启动提取流程 --------------------------
def key_point_extract():
    # 启动交互，接收最终字典
    final_travel_dict = extract_travel_preference()
    
    # 示例：若获取到完整字典，必打印关键信息（修复之前不打印的问题）
    if final_travel_dict:
        return final_travel_dict
    else:
        return None
        