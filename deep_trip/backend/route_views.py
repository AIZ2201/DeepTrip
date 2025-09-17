from flask import Blueprint, render_template, session
from .models import db
from sqlalchemy import text

route_bp = Blueprint('route', __name__)

@route_bp.route('/route/planner')
def route_planner():
    user = session.get('user')
    routes = []
    if user:
        user_id = user.get('id')
        sql = text("SELECT id, start, end, days, budget, tags, description, "
                   "DATE_FORMAT(NOW(), '%Y-%m-%d') as today "
                   "FROM main_route WHERE user_id=:uid ORDER BY id DESC")
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
