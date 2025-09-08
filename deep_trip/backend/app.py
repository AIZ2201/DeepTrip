# app.py
from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from user_login import UserLogin
from user_register import UserRegister
from password_reset import PasswordReset
from datetime import timedelta
import re
import os
from merchant_login import MerchantAuth   # <- 如果你的文件叫 merchant_login.py，就改成 from merchant_login import MerchantAuth

app = Flask(
    __name__,
    template_folder='../frontend/templates',
    static_folder='../frontend/static'
)

app.secret_key = os.getenv('FLASK_SECRET_KEY', 'dev_only_change_me')

# 开发期可为 True；上线必须 False
DEV_EXPOSE_RESET_CODE = True

# ============ 登录 ============
@app.route('/')
@app.route('/user/login', methods=['GET', 'POST'])
def user_login():
    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '').strip()
        remember = request.form.get('remember')

        if not email or not password:
            return jsonify({'success': False, 'message': '邮箱和密码不能为空'})
        if not re.match(r'^[^\s@]+@[^\s@]+\.[^\s@]+$', email):
            return jsonify({'success': False, 'message': '请输入有效的邮箱地址'})

        db = UserLogin()
        if db.check_user_login(email, password):
            # 清理其他身份，避免混用
            session.pop('merchant', None)
            session.pop('admin', None)
            session['user'] = email
            if remember:
                session.permanent = True
                app.permanent_session_lifetime = timedelta(days=30)
            return jsonify({'success': True, 'message': '登录成功'})
        else:
            return jsonify({'success': False, 'message': '邮箱或密码错误'})

    return render_template('user_login.html')

# ============ 注册 ============
@app.route('/user/register', methods=['GET', 'POST'])
def user_register():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip()
        phone = request.form.get('phone', '').strip()
        password = request.form.get('password', '').strip()

        if not all([username, email, phone, password]):
            return jsonify({'success': False, 'message': '所有字段不能为空'})
        if not re.match(r'^[a-zA-Z0-9_]{2,20}$', username):
            return jsonify({'success': False, 'message': '用户名需为2-20位字母/数字/下划线'})
        if not re.match(r'^[^\s@]+@[^\s@]+\.[^\s@]+$', email):
            return jsonify({'success': False, 'message': '请输入有效的邮箱地址'})
        if not re.match(r'^1[3-9]\d{9}$', phone):  # 按你之前逻辑保留大陆手机号校验
            return jsonify({'success': False, 'message': '请输入有效的11位手机号'})
        if len(password) < 8 or len(password) > 20:
            return jsonify({'success': False, 'message': '密码长度需为8-20位'})

        register = UserRegister()
        success, message = register.register_user(username, email, phone, password)
        return jsonify({'success': success, 'message': message})

    return render_template('user_register.html')

# ============ 忘记密码 ============
@app.route('/user/forgot-password', methods=['GET'])
def forgot_password_page():
    return render_template('user_forgot_password.html')

@app.route('/user/forgot-password/send-code', methods=['POST'])
def forgot_password_send_code():
    email = request.form.get('email', '').strip()
    if not email:
        return jsonify({'success': False, 'message': '请输入邮箱'})
    if not re.match(r'^[^\s@]+@[^\s@]+\.[^\s@]+$', email):
        return jsonify({'success': False, 'message': '请输入有效的邮箱地址'})

    svc = PasswordReset()
    if not svc.user_exists(email):
        return jsonify({'success': False, 'message': '该邮箱未注册'})

    code = svc.create_code(email, minutes=10)
    if not code:
        return jsonify({'success': False, 'message': '发送失败，请稍后重试'})

    resp = {'success': True, 'message': '验证码已发送，请查收邮箱'}
    if DEV_EXPOSE_RESET_CODE:
        resp['dev_code'] = code  # 开发期回显，生产删掉
    return jsonify(resp)

@app.route('/user/forgot-password/reset', methods=['POST'])
def forgot_password_reset():
    email = request.form.get('email', '').strip()
    code = request.form.get('code', '').strip()
    new_password = request.form.get('password', '').strip()

    if not all([email, code, new_password]):
        return jsonify({'success': False, 'message': '请完整填写邮箱、验证码和新密码'})
    if not re.match(r'^[^\s@]+@[^\s@]+\.[^\s@]+$', email):
        return jsonify({'success': False, 'message': '请输入有效的邮箱地址'})
    if len(new_password) < 8 or len(new_password) > 20:
        return jsonify({'success': False, 'message': '新密码长度需为8-20位'})

    svc = PasswordReset()
    if not svc.verify_code_valid(email, code):
        return jsonify({'success': False, 'message': '验证码无效或已过期'})

    if not svc.update_user_password_plain(email, new_password):
        return jsonify({'success': False, 'message': '重置密码失败，请稍后重试'})

    svc.mark_code_used(email, code)
    return jsonify({'success': True, 'message': '密码已重置，请使用新密码登录'})

# ---- 模板上下文：current_user ----
@app.context_processor
def inject_current_user():
    cu = None
    if session.get('user'):
        cu = {'email': session.get('user'), 'role': 'traveller'}
    elif session.get('merchant'):
        cu = {'email': session.get('merchant'), 'role': 'merchant'}
    elif session.get('admin'):
        cu = {'email': session.get('admin'), 'role': 'admin'}
    return dict(current_user=cu)

# ============ 商家登录 ============
@app.route('/merchant/login', methods=['GET', 'POST'])
def merchant_login():
    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '').strip()
        remember = request.form.get('remember')

        if not email or not password:
            return jsonify({'success': False, 'message': '邮箱和密码不能为空'})
        if not re.match(r'^[^\s@]+@[^\s@]+\.[^\s@]+$', email):
            return jsonify({'success': False, 'message': '请输入有效的邮箱地址'})

        db = MerchantAuth()
        if db.check_login(email, password):
            session.pop('user', None)
            session.pop('admin', None)
            session['merchant'] = email
            if remember:
                session.permanent = True
                app.permanent_session_lifetime = timedelta(days=30)
            # /merchant/login POST 成功分支
            return jsonify({
                'success': True,
                'message': '登录成功',
                'redirect': url_for('merchant_home')  # 告诉前端跳到哪
            })
        else:
            return jsonify({'success': False, 'message': '邮箱或密码错误，或账号未激活'})

    return render_template('merchant_login.html')

# ------------------- 商家注册：发送验证码 -------------------
@app.route('/merchant/register/send-code', methods=['POST'])
def merchant_register_send_code():
    email = request.form.get('email', '').strip()
    if not email:
        return jsonify({'success': False, 'message': '请输入邮箱'})
    if not re.match(r'^[^\s@]+@[^\s@]+\.[^\s@]+$', email):
        return jsonify({'success': False, 'message': '请输入有效的邮箱地址'})

    svc = MerchantAuth()
    # 如果邮箱已经被注册，直接拒绝（注册场景）
    if svc.exists_by_email(email):
        return jsonify({'success': False, 'message': '该邮箱已被注册'})

    code = svc.create_register_code(email, minutes=10)
    if not code:
        return jsonify({'success': False, 'message': '发送失败，请稍后重试'})

    # TODO: 生产这里发送真实邮件
    # send_email(email, '【旅游小助手】商家注册验证码', f'验证码：{code}，10分钟有效')

    resp = {'success': True, 'message': '验证码已发送，请查收邮箱'}
    if DEV_EXPOSE_RESET_CODE:
        resp['dev_code'] = code
    return jsonify(resp)

# ------------------- 商家注册：提交注册 -------------------
@app.route('/merchant/register', methods=['GET', 'POST'])
def merchant_register():
    if request.method == 'POST':
        business_type = request.form.get('business_type', '').strip()     # hotel/attraction/restaurant/other
        username = request.form.get('username', '').strip()
        phone = request.form.get('phone', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '').strip()
        code = request.form.get('code', '').strip()
        name = request.form.get('name', '').strip() or username  # 店铺名，前端没单独字段的话用用户名占位

        # 基本校验
        if not all([business_type, username, phone, email, password, code]):
            return jsonify({'success': False, 'message': '请完整填写信息'})
        if business_type not in ['hotel','attraction','restaurant','other']:
            return jsonify({'success': False, 'message': '请选择有效的商家类型'})
        if not re.match(r'^[a-zA-Z0-9_\u4e00-\u9fa5]{2,30}$', username):
            return jsonify({'success': False, 'message': '用户名需为2-30位，可含中英文/数字/下划线'})
        if not re.match(r'^1[3-9]\d{9}$', phone):
            return jsonify({'success': False, 'message': '请输入有效的11位手机号'})
        if not re.match(r'^[^\s@]+@[^\s@]+\.[^\s@]+$', email):
            return jsonify({'success': False, 'message': '请输入有效的邮箱地址'})
        if len(password) < 8 or len(password) > 20:
            return jsonify({'success': False, 'message': '密码长度需为8-20位'})

        svc = MerchantAuth()
        # 验证码校验
        if not svc.verify_register_code(email, code):
            return jsonify({'success': False, 'message': '验证码无效或已过期'})

        # 插入商家
        ok, msg = svc.register(username=username, name=name, email=email,
                               phone=phone, password=password, business_type=business_type)
        if ok:
            svc.mark_register_code_used(email, code)
        return jsonify({'success': ok, 'message': msg})

    # GET 渲染页面
    return render_template('merchant_register.html')

# ============ 商家中心（示例） ============
# 在 app.py 里，和其它商家路由放一起
@app.route('/merchant/home')
def merchant_home():
    if not session.get('merchant'):
        return redirect(url_for('merchant_login'))

    # 先给一组示例数据；你也可以直接 render_template('merchant_home.html')
    context = {
        "sales_today": 28650,
        "orders_today": 42,
        "avg_rating": 4.6,
        "total_customers": 1320,
        "latest_reviews": [
            {"username": "张三", "date": "2025-09-06", "rating": 5, "content": "环境很好，体验很棒！"},
            {"username": "李四", "date": "2025-09-05", "rating": 4, "content": "服务热情，下次还来～"},
            {"username": "王五", "date": "2025-09-03", "rating": 4, "content": "总体不错，推荐！"},
        ],
        "pending_tasks": [
            {"title": "确认 3 笔未处理订单", "due_date": "今天 18:00", "priority": "high"},
            {"title": "回复 2 条新评价", "due_date": "今天 20:00", "priority": "medium"},
            {"title": "完善店铺资质材料", "due_date": "本周内", "priority": "low"},
        ],
    }
    return render_template('merchant_home.html', **context)


# ============ 统一退出 ============
@app.route('/user/logout')
def user_logout():
    session.pop('user', None)
    session.pop('merchant', None)
    session.pop('admin', None)
    flash('已成功登出', 'info')
    return redirect(url_for('user_login'))

# ============ 业务页面 ============
@app.route('/route_planner')
def route_planner():
    return render_template('route_planner.html')

@app.route('/ai_chat')
def ai_chat():
    return render_template('ai_chat.html')

@app.route('/booking')
def booking():
    return render_template('booking.html')

# 注意：删除了重复的 /logout 路由

if __name__ == '__main__':
    app.run(debug=True)
