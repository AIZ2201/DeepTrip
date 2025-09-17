from flask import Blueprint, request, jsonify, render_template, session
from ...agent.chat_agent.agent import ChatAgent
from ...agent.chat_agent.key_point_extract import get_response, system_prompt
from .models import db
from sqlalchemy import text
import json

ai_bp = Blueprint('ai', __name__, url_prefix='/ai')

def clean_city(name):
    provinces = ["河北","山西","辽宁","吉林","黑龙江","江苏","浙江","安徽","福建","江西","山东","河南","湖北","湖南","广东","海南","四川","贵州","云南","陕西","甘肃","青海","台湾","内蒙古","广西","宁夏","新疆","西藏","香港","澳门"]
    for p in provinces:
        if name.startswith(p):
            return name.replace(p, "").strip()
    return name

def parse_travel_plan(plan_text):
    """
    解析AI返回的旅游规划文本，提取description、每日行程、预算等信息。
    返回: description(str), days(list of str), budget(str)
    """
    import re
    # description: 首行
    lines = plan_text.strip().splitlines()
    description = ""
    days = []
    budget = ""
    day_section = False
    budget_section = False
    day_buffer = []
    for line in lines:
        if not description and line.strip():
            description = line.strip()
            continue
        if "每日详细行程" in line:
            day_section = True
            continue
        if day_section and (line.strip().startswith("###") or line.strip().startswith("---")):
            continue
        if day_section and re.match(r"^####?\s*DAY\d+", line, re.I):
            if day_buffer:
                days.append('\n'.join(day_buffer).strip())
                day_buffer = []
            day_buffer.append(line)
            continue
        if day_section and (line.strip().startswith("### 预算概算") or "预算概算" in line):
            if day_buffer:
                days.append('\n'.join(day_buffer).strip())
                day_buffer = []
            day_section = False
            budget_section = True
            continue
        if day_section:
            day_buffer.append(line)
        if budget_section:
            budget += line + "\n"
    if day_buffer:
        days.append('\n'.join(day_buffer).strip())
    budget = budget.strip()
    return description, days, budget

@ai_bp.route('/chat', methods=['GET', 'POST'])
def ai_chat():
    if 'ai_state' not in session:
        session['ai_state'] = "collecting"
    if 'ai_travel_dict' not in session:
        session['ai_travel_dict'] = None
    if 'route_id' not in session:
        session['route_id'] = None

    # 聊天历史仅在本地变量，不再存 session
    if 'ai_messages' in session:
        messages = session['ai_messages']
    else:
        messages = [{"role": "system", "content": system_prompt}]
    state = session.get('ai_state', "collecting")
    travel_dict = session.get('ai_travel_dict')
    route_id = session.get('route_id')

    if request.method == 'GET':
        # 首次进入页面
        welcome = "欢迎使用旅游偏好提取助手！请描述你的旅游计划，我会帮你整理（输入'退出'结束）"
        chat_msgs = [{'sender': 'ai', 'content': welcome}]
        session.modified = True
        return render_template('ai_chat.html', chat_sessions=[], chat=None, messages=chat_msgs)

    user_input = request.form.get('user_input', '')
    if user_input is not None:
        user_input = user_input.strip()
    else:
        user_input = ''
    chat_msgs = []
    flag = False

    if user_input or flag == True:
        messages.append({"role": "user", "content": user_input})
        # 只要还没收集到完整字典，就继续交互
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
                session['ai_state'] = "finished"
                state = "finished"
                flag = True

                # 新增：保存路线基本信息到main_route
                user = session.get('user')
                if user:
                    user_id = user.get('id')
                    start = travel_dict.get("出发点", "")[:20]
                    end = travel_dict.get("目的地", "")[:20]
                    # 计算天数
                    days = 1
                    try:
                        in_date = travel_dict.get("行程时间", {}).get("入住日期", "")
                        out_date = travel_dict.get("行程时间", {}).get("离店日期", "")
                        if len(in_date) == 8 and len(out_date) == 8:
                            from datetime import datetime
                            d1 = datetime.strptime(in_date, "%Y%m%d")
                            d2 = datetime.strptime(out_date, "%Y%m%d")
                            days = (d2 - d1).days
                            if days < 1:
                                days = 1
                    except Exception:
                        days = 1
                    budget = str(travel_dict.get("经费预算", ""))[:20]
                    tags = ",".join(travel_dict.get("特殊需求", []))[:255]
                    conn = None
                    try:
                        conn = db.engine.raw_connection()
                        with conn.cursor() as cur:
                            cur.execute(
                                "INSERT INTO main_route (user_id, start, end, days, budget, tags, description) VALUES (%s,%s,%s,%s,%s,%s,'')",
                                (user_id, start, end, days, budget, tags)
                            )
                            conn.commit()
                            cur.execute("SELECT LAST_INSERT_ID()")
                            rid = cur.fetchone()[0]
                            session['route_id'] = rid
                    except Exception as e:
                        import traceback
                        print("插入main_route异常:", e)
                        traceback.print_exc()
                        session['route_id'] = None
                    finally:
                        if conn:
                            conn.close()
                else:
                    # 未登录用户不保存路线
                    session['route_id'] = None
                ai_reply = "已获取你的完整旅游偏好，整理如下：<br>" + json.dumps(travel_dict, ensure_ascii=False, indent=2) + "<br>输入任意内容后为您生成完整旅游规划"
            else:
                ai_reply = assistant_content
        else:
            # 已收集完毕，直接调用 ChatAgent 生成规划
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

                # 仅在已登录且有 route_id 时自动保存
                user = session.get('user')
                route_id = session.get('route_id')
                if user and route_id and travel_plan:
                    conn = db.engine.raw_connection()
                    try:
                        with conn.cursor() as cur:
                            # 直接存储完整 travel_plan，不做截断
                            cur.execute("UPDATE main_route SET description=%s WHERE id=%s", (travel_plan, route_id))
                            conn.commit()
                    except Exception as e:
                        import traceback
                        print("自动保存行程异常:", e)
                        traceback.print_exc()
                    finally:
                        conn.close()
            except Exception as e:
                import traceback
                traceback.print_exc()
                ai_reply = "生成旅游规划时发生错误，请稍后重试。"
        chat_msgs.append({'sender': 'user', 'content': user_input})
        chat_msgs.append({'sender': 'ai', 'content': ai_reply})
        # 只保存最近10条消息到 session，防止 session 过大
        session['ai_messages'] = messages[-10:]
        session.modified = True
        return jsonify({'user_input': user_input, 'ai_reply': ai_reply})

    # GET 或无输入时
    chat_msgs = []
    for m in messages[1:]:
        if m['role'] == 'user':
            chat_msgs.append({'sender': 'user', 'content': m['content']})
        elif m['role'] == 'assistant':
            chat_msgs.append({'sender': 'ai', 'content': m['content']})
    # 只保存最近10条消息到 session
    session['ai_messages'] = messages[-10:]
    session.modified = True
    return render_template('ai_chat.html', chat_sessions=[], chat=None, messages=chat_msgs)