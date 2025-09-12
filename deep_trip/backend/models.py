from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'user_login'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), unique=True, nullable=False)
    email = db.Column(db.String(64), unique=True, nullable=False)
    phonenumber = db.Column(db.String(16), unique=True, nullable=True)
    password = db.Column(db.String(64), nullable=False)
    # ...existing code...

class Feedback(db.Model):
    __tablename__ = 'feedback'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user_login.id'), nullable=False)
    service_type = db.Column(db.String(32), nullable=False)
    service_id = db.Column(db.String(64), nullable=False)
    service_name = db.Column(db.String(128), nullable=True)
    overall_rating = db.Column(db.Integer, nullable=False)
    environment_rating = db.Column(db.Integer, nullable=True)
    service_rating = db.Column(db.Integer, nullable=True)
    value_rating = db.Column(db.Integer, nullable=True)
    feedback_content = db.Column(db.Text, nullable=False)
    images = db.Column(db.Text, nullable=True)  # 建议存json字符串
    created_at = db.Column(db.DateTime, nullable=False)
    merchant_feedback = db.Column(db.Text, nullable=True)
    merchant_reply_time = db.Column(db.DateTime, nullable=True)
    # ...existing code...

class Admin(db.Model):
    __tablename__ = 'admin'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), unique=True, nullable=False)
    email = db.Column(db.String(64), unique=True, nullable=False)
    password = db.Column(db.String(64), nullable=False)
    # ...existing code...