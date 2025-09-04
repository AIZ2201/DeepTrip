from flask import Flask
import os
import configparser
from models import db  # 只导入db

app = Flask(__name__, template_folder='../frontend/templates', static_folder='../frontend/static')
app.secret_key = 'this_is_secret_key'

config = configparser.ConfigParser()
config.read(os.path.join(os.path.dirname(__file__), 'db_config.ini'), encoding='utf-8')
db_password = config.get('mysql', 'password', fallback='')

app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://root:{db_password}@localhost:3306/deeptrip?charset=utf8mb4"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)  # 用init_app绑定

# 注册蓝图
from user_views import user_bp
from merchant_views import merchant_bp
from admin_views import admin_bp
from route_views import route_bp
from ai_views import ai_bp
from booking_views import booking_bp
from feedback_views import feedback_bp

app.register_blueprint(user_bp)
app.register_blueprint(merchant_bp)
app.register_blueprint(admin_bp)
app.register_blueprint(route_bp)
app.register_blueprint(ai_bp)
app.register_blueprint(booking_bp)
app.register_blueprint(feedback_bp)

if __name__ == '__main__':
    app.run(debug=True)
app.register_blueprint(merchant_bp)
app.register_blueprint(admin_bp)
app.register_blueprint(route_bp)
app.register_blueprint(ai_bp)
app.register_blueprint(booking_bp)
app.register_blueprint(feedback_bp)

if __name__ == '__main__':
    app.run(debug=True)
