from flask import Blueprint, render_template, session, request, jsonify
from .models import db
from sqlalchemy import text
from ...agent.chat_agent.agent import ChatAgent

route_bp = Blueprint('route', __name__)

@route_bp.route('/route/planner', methods=['GET', 'POST'])
def route_planner():
    user = session.get('user')
    if request.method == 'POST':
        if not user:
            return jsonify({'success': False, 'msg': '请先登录'})
        user_id = user.get('id')
        # 获取表单数据
        start = request.form.get('start_city', '').strip()
        end = request.form.get('end_city', '').strip()
        start_date = request.form.get('start_date', '').replace('-', '')
        end_date = request.form.get('end_date', '').replace('-', '')
        budget = request.form.get('budget', '').strip()
        tags = request.form.getlist('interests')
        tags_str = ','.join(tags)
        # 校验
        if not (start and end and start_date and end_date and budget):
            return jsonify({'success': False, 'msg': '请填写所有必填项'})
        # 计算天数
        days = 1
        try:
            from datetime import datetime
            d1 = datetime.strptime(start_date, "%Y%m%d")
            d2 = datetime.strptime(end_date, "%Y%m%d")
            days = (d2 - d1).days
            if days < 1:
                days = 1
        except Exception:
            days = 1

        # 分类tags
        scenic_types = ['自然风光', '历史文化', '户外探险', '艺术展览']
        accommodation_types = ['亲子活动']  # 可扩展
        special_types = ['美食探索', '购物血拼', '休闲度假']  # 可扩展
        scenic_type_pref = []
        accommodation_pref = []
        special_pref = []
        for tag in tags:
            if tag in scenic_types:
                scenic_type_pref.append(tag)
            elif tag in accommodation_types:
                accommodation_pref.append(tag)
            elif tag in special_types:
                special_pref.append(tag)
        if not scenic_type_pref:
            scenic_type_pref = ["未明确"]
        if not accommodation_pref:
            accommodation_pref = ["未明确"]
        if not special_pref:
            special_pref = ["未明确"]

        # 构造 travel_dict
        travel_dict = {
            "出发点": start,
            "目的地": end,
            "行程时间": {
                "入住日期": start_date,
                "离店日期": end_date
            },
            "经费预算": budget,
            "景点类型偏好": scenic_type_pref,
            "住宿需求": accommodation_pref,
            "特殊需求": special_pref
        }
        # 生成 travel_plan（完整流程）
        try:
            agent = ChatAgent()
            agent.travel_dict = travel_dict
            travel_info = agent.get_travel_info(travel_dict)
            path = agent.get_path_info()
            hotel_info = agent.get_hotel_info(top_n=5)
            tourism_info = agent.get_tourism_info()
            food_info = agent.get_food_info()
            travel_plan = agent.generate_comprehensive_travel_plan()
        except Exception as e:
            import traceback
            traceback.print_exc()
            return jsonify({'success': False, 'msg': 'AI生成路线失败'})
        # 存入数据库
        conn = db.engine.raw_connection()
        try:
            with conn.cursor() as cur:
                cur.execute(
                    "INSERT INTO main_route (user_id, start, end, days, budget, tags, description) VALUES (%s,%s,%s,%s,%s,%s,%s)",
                    (user_id, start, end, days, budget, tags_str, travel_plan)
                )
                conn.commit()
                cur.execute("SELECT LAST_INSERT_ID()")
                rid = cur.fetchone()[0]
            # 返回新路线数据
            return jsonify({
                'success': True,
                'route': {
                    'id': rid,
                    'start': start,
                    'end': end,
                    'days': days,
                    'budget': budget,
                    'tags': tags_str,
                    'description': travel_plan
                }
            })
        except Exception as e:
            conn.rollback()
            import traceback
            traceback.print_exc()
            return jsonify({'success': False, 'msg': '数据库保存失败'})
        finally:
            conn.close()
    # GET
    routes = []
    if user:
        user_id = user.get('id')
        sql = text("SELECT id, start, end, days, budget, tags, description FROM main_route WHERE user_id=:uid ORDER BY id DESC")
        result = db.session.execute(sql, {'uid': user_id})
        for row in result:
            routes.append({
                'id': row.id,
                'start': row.start,
                'end': row.end,
                'days': row.days,
                'budget': row.budget,
                'tags': row.tags,
                'description': row.description or '',
            })
    return render_template('route_planner.html', routes=routes)
