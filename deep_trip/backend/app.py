from flask import Flask, render_template, request, redirect, url_for, flash, session

app = Flask(__name__, template_folder='../frontend/templates', static_folder='../frontend/static')
app.secret_key = 'your_secret_key'  # 用于session和flash

# TODO: 这里预留MySQL连接，后续可用SQLAlchemy或pymysql实现
# from flask_sqlalchemy import SQLAlchemy
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://user:password@localhost/dbname'
# db = SQLAlchemy(app)

@app.route('/')
def index():
    return redirect(url_for('user_login'))

@app.route('/user/login', methods=['GET', 'POST'])
def user_login():
    if request.method == 'POST':
        # email = request.form['email']
        # password = request.form['password']
        # TODO: 校验用户登录（数据库校验）
        # if valid:
        #     session['user'] = email
        #     return redirect(url_for('user_dashboard'))
        # else:
        #     flash('邮箱或密码错误', 'error')
        flash('模拟登录成功', 'success')
        return redirect(url_for('user_login'))
    return render_template('user_login.html')

@app.route('/user/register', methods=['GET', 'POST'])
def user_register():
    if request.method == 'POST':
        # username = request.form['username']
        # email = request.form['email']
        # phone = request.form['phone']
        # password = request.form['password']
        # TODO: 写入数据库
        flash('模拟注册成功', 'success')
        return redirect(url_for('user_login'))
    return render_template('user_register.html')

@app.route('/merchant/login', methods=['GET', 'POST'])
def merchant_login():
    if request.method == 'POST':
        # email = request.form['email']
        # password = request.form['password']
        # TODO: 校验商户登录
        flash('模拟商户登录成功', 'success')
        return redirect(url_for('merchant_login'))
    return render_template('merchant_login.html')

@app.route('/merchant/register', methods=['GET', 'POST'])
def merchant_register():
    if request.method == 'POST':
        # TODO: 商户注册逻辑
        flash('模拟商户注册成功', 'success')
        return redirect(url_for('merchant_login'))
    return render_template('merchant_register.html')

@app.route('/route_planner')
def route_planner():
    return render_template('route_planner.html')

@app.route('/ai_chat')
def ai_chat():
    return render_template('ai_chat.html')

@app.route('/booking')
def booking():
    return render_template('booking.html')

@app.route('/feedback')
def feedback():
    return render_template('feedback.html')

@app.route('/merchant_info_upload')
def merchant_info_upload():
    return render_template('merchant_info_upload.html')

@app.route('/merchant_feedback')
def merchant_feedback():
    return render_template('merchant_feedback.html')

@app.route('/admin_login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        # TODO: 管理员登录逻辑
        flash('模拟管理员登录成功', 'success')
        return redirect(url_for('admin_dashboard'))
    return render_template('admin_login.html')

@app.route('/admin_dashboard')
def admin_dashboard():
    return render_template('admin_dashboard.html')

@app.route('/admin_merchant_review')
def admin_merchant_review():
    return render_template('admin_merchant_review.html')

@app.route('/admin_data_report')
def admin_data_report():
    return render_template('admin_data_report.html')

# 其他页面可按需添加

if __name__ == '__main__':
    app.run(debug=True)
