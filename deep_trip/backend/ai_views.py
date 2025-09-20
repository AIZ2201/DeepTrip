from flask import Blueprint, request, jsonify, render_template, session
from ...agent.chat_agent.agent import ChatAgent
from ...agent.chat_agent.key_point_extract import get_response, system_prompt
import json

ai_bp = Blueprint('ai', __name__, url_prefix='/ai')

def clean_city(name):
    provinces = [
        "河北","山西","辽宁","吉林","黑龙江","江苏","浙江","安徽","福建","江西","山东",
        "河南","湖北","湖南","广东","海南","四川","贵州","云南","陕西","甘肃","青海",
        "台湾","内蒙古","广西","宁夏","新疆","西藏","香港","澳门"
    ]
    for p in provinces:
        if name.startswith(p):
            return name.replace(p, "").strip()
    return name

@ai_bp.route('/chat', methods=['GET', 'POST'])
def ai_chat():
    # 初始化session
    if 'ai_messages' not in session:
        session['ai_messages'] = [{"role": "system", "content": system_prompt}]
        session['ai_state'] = "collecting"
        session['ai_travel_dict'] = None

    messages = session['ai_messages']
    state = session.get('ai_state', "collecting")
    travel_dict = session.get('ai_travel_dict')

    if request.method == 'GET':
        # 首次进入页面
        welcome = "欢迎使用旅游偏好提取助手！请描述你的旅游计划，我会帮你整理（输入'退出'结束）"
        chat_msgs = [{'sender': 'ai', 'content': welcome}]
        session.modified = True
        return render_template('ai_chat.html', chat_sessions=[], chat=None, messages=chat_msgs)

    user_input = request.form.get('user_input', '').strip()
    chat_msgs = []
    flag = False

    if user_input or flag:
        messages.append({"role": "user", "content": user_input})

        # 信息收集阶段
        if state == "collecting":
            response = get_response(messages)
            assistant_content = response.choices[0].message.content
            messages.append({"role": "assistant", "content": assistant_content})

            # 判断是否为最终字典
            is_final_dict = (
                "{" in assistant_content and "}" in assistant_content
                and all(key in assistant_content for key in ["出发点", "目的地", "行程时间"])
                and "入住日期" in assistant_content and "离店日期" in assistant_content
            )
            if is_final_dict:
                dict_start = assistant_content.find("{")
                dict_end = assistant_content.rfind("}") + 1
                dict_str = assistant_content[dict_start:dict_end].replace("'", "\"").replace("\\", "")
                travel_dict = json.loads(dict_str)
                travel_dict["出发点"] = clean_city(travel_dict["出发点"])
                travel_dict["目的地"] = clean_city(travel_dict["目的地"])
                for key in ["住宿需求", "特殊需求"]:
                    if travel_dict.get(key) == ["无"]:
                        travel_dict[key] = ["未明确"]
                session['ai_travel_dict'] = travel_dict
                # 格式化关键信息供用户确认
                confirm_text = (
                    f"请确认以下信息：<br>"
                    f"出发点：{travel_dict.get('出发点','')}<br>"
                    f"目的地：{travel_dict.get('目的地','')}<br>"
                    f"入住日期：{travel_dict.get('行程时间',{}).get('入住日期','')}<br>"
                    f"离店日期：{travel_dict.get('行程时间',{}).get('离店日期','')}<br>"
                    f"住宿需求：{'、'.join(travel_dict.get('住宿需求',[]))}<br>"
                    f"特殊需求：{'、'.join(travel_dict.get('特殊需求',[]))}<br>"
                    f"经费预算：{travel_dict.get('经费预算','')}<br>"
                    f"如无误，请输入“确认”或任意内容继续。"
                )
                ai_reply = confirm_text
                session['ai_state'] = "wait_confirm"
            else:
                ai_reply = assistant_content

        # 等待用户确认阶段
        elif state == "wait_confirm":
            travel_dict = session.get('ai_travel_dict')
            if not travel_dict:
                ai_reply = "会话已失效，请刷新页面重新开始。"
                session.clear()
                return jsonify({'user_input': user_input, 'ai_reply': ai_reply})
            # 保存路线基本信息到main_route（如有需要可补充）
            session['ai_state'] = "confirm"
            ai_reply = "如需生成完整旅游规划，请输入“生成”或任意内容继续。"

        # 生成完整规划阶段
        elif state == "confirm":
            travel_dict = session.get('ai_travel_dict')
            if not travel_dict:
                ai_reply = "会话已失效，请刷新页面重新开始。"
                session.clear()
                return jsonify({'user_input': user_input, 'ai_reply': ai_reply})
            try:
                agent = ChatAgent()
                travel_info = agent.get_travel_info(travel_dict)
                path = agent.get_path_info()
                hotel_info = agent.get_hotel_info(top_n=5)
                tourism_info = agent.get_tourism_info()
                food_info = agent.get_food_info()
                travel_plan = agent.generate_comprehensive_travel_plan()
                ai_reply = f"{travel_plan}"
                session['ai_state'] = "finished"
            except Exception as e:
                import traceback
                traceback.print_exc()
                ai_reply = "生成旅游规划时发生错误，请稍后重试。"

        else:
            # 已生成规划后继续对话
            ai_reply = "如需重新规划，请刷新页面。"

        chat_msgs.append({'sender': 'user', 'content': user_input})
        chat_msgs.append({'sender': 'ai', 'content': ai_reply})
        session['ai_messages'] = messages
        session.modified = True
        return jsonify({'user_input': user_input, 'ai_reply': ai_reply})

    # GET 或无输入时，回显历史
    chat_msgs = []
    for m in messages[1:]:
        if m['role'] == 'user':
            chat_msgs.append({'sender': 'user', 'content': m['content']})
        elif m['role'] == 'assistant':
            chat_msgs.append({'sender': 'ai', 'content': m['content']})
    return render_template('ai_chat.html', chat_sessions=[], chat=None, messages=chat_msgs)