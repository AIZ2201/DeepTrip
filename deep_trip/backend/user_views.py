from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from models import db, User  # 只从models导入

user_bp = Blueprint('user', __name__)

@user_bp.route('/')
def index():
    return redirect(url_for('user.user_login'))

@user_bp.route('/user/login', methods=['GET', 'POST'])
def user_login():
    if request.method == 'POST':
        email = request.form['email'].strip()
        password = request.form['password'].strip()
        user = User.query.filter_by(email=email, password=password).first()
        if user:
            session['user_id'] = user.id
            session['username'] = user.username
            flash('登录成功', 'success')
            return redirect(url_for('route.route_planner'))
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
    return render_template('user_register.html')
