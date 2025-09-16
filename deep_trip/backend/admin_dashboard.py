from flask import Blueprint, render_template, session, redirect, url_for
from models import db, User, Merchant

admin_dashboard_bp = Blueprint('admin_dashboard', __name__)

@admin_dashboard_bp.route('/admin/dashboard')
def dashboard():
    # 登录校验
    if 'admin' not in session or not session['admin']:
        return redirect(url_for('admin.admin_login'))
    # 查询总用户数
    total_users = db.session.query(User).count()
    # 查询活跃商户数
    active_merchants = db.session.query(Merchant).filter(Merchant.status == 'active').count()
    # 订单和交易额暂未实现
    orders_today = 0
    total_amount = 0
    return render_template('admin_dashboard.html',
        total_users=total_users,
        active_merchants=active_merchants,
        orders_today=orders_today,
        total_amount=total_amount
    )