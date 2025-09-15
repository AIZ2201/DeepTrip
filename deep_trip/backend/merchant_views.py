from flask import Blueprint, render_template, request, redirect, url_for, flash, session, jsonify
from models import db
from merchant_login import MerchantAuth
from sqlalchemy import text
from datetime import datetime, timedelta, date
import re

merchant_bp = Blueprint('merchant', __name__)

@merchant_bp.route('/merchant/login', methods=['GET', 'POST'])
def merchant_login():
    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '').strip()
        remember = request.form.get('remember')
        if not email or not password:
            return jsonify({'success': False, 'message': '邮箱和密码不能为空'})
        if not re.match(r'^[^\s@]+@[^\s@]+\.[^\s@]+$', email):
            return jsonify({'success': False, 'message': '请输入有效的邮箱地址'})
        db_auth = MerchantAuth()
        if db_auth.check_login(email, password):
            session.pop('user', None)
            session.pop('admin', None)
            merchant_row = db.session.execute(text('SELECT * FROM merchant_login WHERE email=:email'), {'email': email}).fetchone()
            if merchant_row:
                session['merchant'] = dict(merchant_row._mapping)
            else:
                session['merchant'] = {'email': email}
            if remember:
                session.permanent = True
                merchant_bp.permanent_session_lifetime = timedelta(days=30)
            return jsonify({
                'success': True,
                'message': '登录成功',
                'redirect': url_for('merchant.merchant_home')
            })
        else:
            session['merchant'] = None
            return jsonify({'success': False, 'message': '邮箱或密码错误，或账号未激活'})
    return render_template('merchant_login.html')

@merchant_bp.route('/merchant/home')
def merchant_home():
    merchant = session.get('merchant')
    if not isinstance(merchant, dict):
        return redirect(url_for('merchant.merchant_login'))
    merchant_id = merchant.get('id')
    today = date.today()
    yesterday = today - timedelta(days=1)
    week_start = today - timedelta(days=today.weekday())
    last_week_start = week_start - timedelta(days=7)
    last_week_end = week_start - timedelta(days=1)
    sales_today = db.session.execute(text('SELECT COALESCE(SUM(amount),0) FROM merchant_order WHERE merchant_id=:mid AND DATE(order_time)=:dt'), {'mid': merchant_id, 'dt': today}).scalar()
    sales_yesterday = db.session.execute(text('SELECT COALESCE(SUM(amount),0) FROM merchant_order WHERE merchant_id=:mid AND DATE(order_time)=:dt'), {'mid': merchant_id, 'dt': yesterday}).scalar()
    orders_today = db.session.execute(text('SELECT COUNT(*) FROM merchant_order WHERE merchant_id=:mid AND DATE(order_time)=:dt'), {'mid': merchant_id, 'dt': today}).scalar()
    orders_yesterday = db.session.execute(text('SELECT COUNT(*) FROM merchant_order WHERE merchant_id=:mid AND DATE(order_time)=:dt'), {'mid': merchant_id, 'dt': yesterday}).scalar()
    # 将service_id改为merchant_id
    avg_rating = db.session.execute(text('SELECT AVG(overall_rating) FROM feedback WHERE merchant_id=:mid AND created_at>=:start AND created_at<=:end'), {'mid': str(merchant_id), 'start': week_start, 'end': today}).scalar() or 0
    avg_rating_last = db.session.execute(text('SELECT AVG(overall_rating) FROM feedback WHERE merchant_id=:mid AND created_at>=:start AND created_at<=:end'), {'mid': str(merchant_id), 'start': last_week_start, 'end': last_week_end}).scalar() or 0
    sales_change = f"{int(sales_today-sales_yesterday)/max(1,sales_yesterday)*100:.0f}%" if sales_yesterday else "N/A"
    orders_change = f"{int(orders_today-orders_yesterday)}" if orders_yesterday else "N/A"
    rating_change = f"{avg_rating-avg_rating_last:.1f}" if avg_rating_last else "N/A"
    return render_template('merchant_home.html',
        sales_today=sales_today,
        sales_change=sales_change,
        orders_today=orders_today,
        orders_change=orders_change,
        avg_rating=round(avg_rating,1),
        rating_change=rating_change
    )

@merchant_bp.route('/merchant/info/upload')
def merchant_info_upload():
    return render_template('merchant_info_upload.html')

@merchant_bp.route('/merchant/feedback')
def merchant_feedback():
    return render_template('merchant_feedback.html')

@merchant_bp.route('/merchant/register', methods=['GET'])
def merchant_register_page():
    return render_template('merchant_register.html')