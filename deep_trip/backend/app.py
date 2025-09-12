# app.py
from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from user_views import user_bp
from datetime import timedelta
import os
from merchant_login import MerchantAuth   # <- 如果你的文件叫 merchant_login.py，就改成 from merchant_login import MerchantAuth
from feedback_views import feedback_bp
from merchant_feedback import merchant_feedback_bp
from merchant_info_upload import merchant_info_bp
from merchant_booking import merchant_booking_bp
from admin_views import admin_bp
from models import db
from sqlalchemy import text
from datetime import datetime, timedelta, date
from merchant_views import merchant_bp
from booking_views import booking_bp
from ai_views import ai_bp
from route_views import route_bp

app = Flask(
    __name__,
    template_folder='../frontend/templates',
    static_folder='../frontend/static'
)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:123456@localhost/deeptrip?charset=utf8mb4'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.secret_key = os.getenv('FLASK_SECRET_KEY', 'dev_only_change_me')

# 绑定 SQLAlchemy 实例到 Flask app
db.init_app(app)

# 开发期可为 True；上线必须 False
DEV_EXPOSE_RESET_CODE = True

# 注册蓝图
app.register_blueprint(feedback_bp)
app.register_blueprint(merchant_feedback_bp)
app.register_blueprint(merchant_info_bp)
app.register_blueprint(merchant_booking_bp)
app.register_blueprint(merchant_bp)
app.register_blueprint(user_bp)
app.register_blueprint(booking_bp)
app.register_blueprint(ai_bp)
app.register_blueprint(route_bp)
app.register_blueprint(admin_bp)

# ============ 统一退出 ============
@app.route('/user/logout')
def user_logout():
    session.pop('user', None)
    session.pop('merchant', None)
    session.pop('admin', None)
    flash('已成功登出', 'info')
    return redirect(url_for('user.user_login'))

if __name__ == '__main__':
    app.run(debug=True)
