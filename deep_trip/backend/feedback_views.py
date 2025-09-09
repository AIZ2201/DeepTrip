from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from models import db, Feedback, User  # 假设你的模型名为 Feedback, User
import datetime
import json

feedback_bp = Blueprint('feedback', __name__)

@feedback_bp.route('/feedback', methods=['GET', 'POST'])
def feedback():
    user = session.get('user')
    if not user:
        flash('请先登录后再评价', 'error')
        return redirect(url_for('user_login'))
    user_id = user.get('id')
    if request.method == 'POST':
        service_type = request.form.get('service_type', '')
        service_id = request.form.get('feedback_target', '')
        service_name = request.form.get('service_name', '')
        overall_rating = request.form.get('overall_rating', 0)
        environment_rating = request.form.get('environment_rating', 0)
        service_rating = request.form.get('service_rating', 0)
        value_rating = request.form.get('value_rating', 0)
        feedback_content = request.form.get('feedback_content', '')
        images = request.form.getlist('images')  # 前端可用隐藏域或ajax传图片路径
        images_json = json.dumps(images) if images else ''
        created_at = datetime.datetime.now()
        fb = Feedback(
            user_id=user_id,
            service_type=service_type,
            service_id=service_id,
            service_name=service_name,
            overall_rating=overall_rating,
            environment_rating=environment_rating,
            service_rating=service_rating,
            value_rating=value_rating,
            feedback_content=feedback_content,
            images=images_json,
            created_at=created_at
        )
        db.session.add(fb)
        db.session.commit()
        flash('评论提交成功！', 'success')
        return redirect(url_for('feedback.feedback'))
    # GET: 查询当前用户的所有评论
    comments = Feedback.query.filter_by(user_id=user_id).order_by(Feedback.created_at.desc()).all()
    # 查询用户信息
    user_info = User.query.get(user_id)
    return render_template('feedback.html', comments=comments, user_info=user_info)
