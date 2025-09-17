from flask import Blueprint, render_template, request, redirect, url_for, flash, session, jsonify
from .models import db, Admin, User, Merchant
from .admin_login import AdminLogin
from datetime import datetime, timedelta, date
from sqlalchemy import text
import re

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '').strip()
        print(email+" and "+password)
        if not email or not password:
            return jsonify({'success': False, 'message': '邮箱和密码不能为空'})
        if not re.match(r'^[^\s@]+@[^\s@]+\.[^\s@]+$', email):
            return jsonify({'success': False, 'message': '请输入有效的邮箱地址'})
        db_admin = AdminLogin()
        if db_admin.check_admin_login(email, password):
            session.pop('user', None)
            session.pop('merchant', None)
            admin_row = db.session.execute(text('SELECT * FROM admin_login WHERE email=:email'), {'email': email}).fetchone()
            if admin_row:
                session['admin'] = dict(admin_row._mapping)
            else:
                session['admin'] = {'email': email}
            return jsonify({
                'success': True,
                'message': '登录成功',
                'redirect': url_for('admin_dashboard.dashboard')
            })
        else:
            session['admin'] = None
            return jsonify({'success': False, 'message': '邮箱或密码错误，或账号未激活'})
    return render_template('admin_login.html')

@admin_bp.route('/admin/merchant/review')
def admin_merchant_review():
    return render_template('admin_merchant_review.html')