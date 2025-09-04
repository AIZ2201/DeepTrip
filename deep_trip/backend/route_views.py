from flask import Blueprint, render_template

route_bp = Blueprint('route', __name__)

@route_bp.route('/route/planner')
def route_planner():
    return render_template('route_planner.html')
