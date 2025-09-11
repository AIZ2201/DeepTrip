from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from models import db, User  # 只从models导入

user_bp = Blueprint('user', __name__)

@user_bp.route('/')
def index():
    return redirect(url_for('user.user_login'))

@user_bp.route('/user/home')
def user_home():
    # 示例：可根据实际需求返回 recent_activities
    recent_activities = [
        {"icon": "🗺️", "title": "规划了新路线", "time": "2025-09-09 10:23"},
        {"icon": "💬", "title": "咨询了AI助手", "time": "2025-09-08 16:45"},
    ]
    return render_template('user_home.html', recent_activities=recent_activities)

@user_bp.route('/user/login', methods=['GET', 'POST'])
def user_login():
    if request.method == 'POST':
        email = request.form['email'].strip()
        password = request.form['password'].strip()
        user = User.query.filter_by(email=email, password=password).first()
        if user:
            session['user'] = {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'phonenumber': user.phonenumber,
                'password': user.password
            }
            flash('登录成功', 'success')
            return redirect(url_for('user.user_home'))
        else:
            flash('邮箱或密码错误', 'error')
            return redirect(url_for('user.user_login'))
    return render_template('user_login.html')

@user_bp.route('/user/register', methods=['GET', 'POST'])
def user_register():
    if request.method == 'POST':
        username = request.form['username'].strip()
        email = request.form['email'].strip()
        phone = request.form['phone'].strip()
        password = request.form['password'].strip()
        if not username or not email or not phone or not password:
            flash('请填写完整信息', 'error')
            return redirect(url_for('user.user_register'))
        if User.query.filter((User.username == username) | (User.email == email) | (User.phone == phone)).first():
            flash('用户名、邮箱或手机号已被注册', 'error')
            return redirect(url_for('user.user_register'))
        user = User(username=username, email=email, phone=phone, password=password)
        db.session.add(user)
        db.session.commit()
        flash('注册成功，请登录', 'success')
        return redirect(url_for('user.user_login'))
    return render_template('user_register.html')

@user_bp.app_context_processor
def inject_current_user():
    cu = None
    user = session.get('user')
    if isinstance(user, dict):
        cu = user
    elif isinstance(session.get('merchant'), dict):
        cu = session.get('merchant')
    elif session.get('admin'):
        cu = {'email': session.get('admin'), 'role': 'admin'}
    return dict(current_user=cu)
