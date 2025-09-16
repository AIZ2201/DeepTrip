from flask import Blueprint, request, jsonify, render_template, session
from models import db, AIChatSession, AIChatMessage, User
from datetime import datetime
import sys
import os

# 保证 agent 包可导入
AGENT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../agent'))
if AGENT_DIR not in sys.path:
    sys.path.insert(0, AGENT_DIR)
from agent.chat_agent.agent import ChatAgent
from agent.chat_agent.key_point_extract import key_point_extract

ai_bp = Blueprint('ai', __name__, url_prefix='/ai')

@ai_bp.route('/chat', methods=['GET', 'POST'])
def ai_chat():
    chat_id = request.args.get('chat_id') or request.form.get('chat_id')
    user_input = request.form.get('user_input')
    chat_sessions = AIChatSession.query.order_by(AIChatSession.updated_at.desc()).all()
    chat = None
    messages = []

    if chat_id:
        chat = AIChatSession.query.get(chat_id)
        if chat:
            messages = AIChatMessage.query.filter_by(session_id=chat.id).order_by(AIChatMessage.created_at).all()

    # 首次进入页面且无消息，直接用模型返回的内容作为欢迎语
    if not messages and request.method == 'GET':
        agent = ChatAgent()
        travel_dict = key_point_extract()
        # 假设 agent.get_travel_info 或其它方法能返回欢迎语（如case.txt首句）
        welcome = agent.get_travel_info(travel_dict)
        messages = [{'sender': 'ai', 'content': welcome}]

    if request.method == 'POST' and user_input:
        if not chat:
            chat = AIChatSession(
                user_id=session.get('user', {}).get('id') if session.get('user') else None,
                title=user_input[:20],
                created_at=datetime.now(),
                updated_at=datetime.now(),
                status='active'
            )
            db.session.add(chat)
            db.session.commit()
            # 首条AI消息用模型返回内容
            agent = ChatAgent()
            travel_dict = key_point_extract()
            welcome = agent.get_travel_info(travel_dict)
            ai_msg = AIChatMessage(
                session_id=chat.id,
                sender='ai',
                content=welcome,
                created_at=datetime.now()
            )
            db.session.add(ai_msg)
            db.session.commit()
            messages = [ai_msg]

        # 保存用户消息
        user_msg = AIChatMessage(
            session_id=chat.id,
            sender='user',
            content=user_input,
            created_at=datetime.now()
        )
        db.session.add(user_msg)
        db.session.commit()

        # 构造历史对话文本（case.txt格式）
        msgs = AIChatMessage.query.filter_by(session_id=chat.id).order_by(AIChatMessage.created_at).all()
        history = ""
        for m in msgs:
            if m.sender == 'user':
                history += f"你：{m.content}\n"
            else:
                history += f"助手：{m.content}\n"
        # 加上本次用户输入
        history += f"你：{user_input}\n"

        # 用 ChatAgent 处理对话
        agent = ChatAgent()
        travel_dict = key_point_extract()
        travel_info = agent.get_travel_info(travel_dict)
        path = agent.get_path_info()
        hotel_info = agent.get_hotel_info(top_n=5)
        tourism_info = agent.get_tourism_info()
        food_info = agent.get_food_info()
        travel_plan = agent.generate_comprehensive_travel_plan()
        ai_reply = (
            f"{travel_info}\n"
            f"{path}\n"
            f"{hotel_info}\n"
            f"{tourism_info}\n"
            f"{food_info}\n"
            f"{'='*50}\n"
            f"{travel_plan}"
        )
        ai_msg = AIChatMessage(
            session_id=chat.id,
            sender='ai',
            content=ai_reply,
            created_at=datetime.now()
        )
        db.session.add(ai_msg)
        db.session.commit()
        return jsonify({'chat_id': chat.id})

    return render_template(
        'ai_chat.html',
        chat_sessions=chat_sessions,
        chat=chat,
        messages=messages
    )

