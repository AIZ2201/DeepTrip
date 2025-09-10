from flask import Blueprint, render_template, session, redirect, url_for
from models import db, Feedback, User
from sqlalchemy import func
import datetime
import json

merchant_feedback_bp = Blueprint('merchant_feedback', __name__)

@merchant_feedback_bp.route('/merchant/feedback')
def merchant_feedback():
    merchant_id = session.get('merchant')
    if not merchant_id:
        return redirect(url_for('merchant_login'))
    # 查询所有与当前商家相关的反馈
    feedbacks = Feedback.query.filter_by(service_id=str(merchant_id)).order_by(Feedback.created_at.desc()).all()
    # 处理 images 字段和 user 信息
    for fb in feedbacks:
        try:
            fb.images_list = json.loads(fb.images) if fb.images else []
        except Exception:
            fb.images_list = []
        fb.user = User.query.get(fb.user_id)
    total_count = len(feedbacks)
    # 评分统计
    if total_count > 0:
        avg_rating = round(sum(f.overall_rating for f in feedbacks) / total_count, 2)
        good_count = sum(1 for f in feedbacks if f.overall_rating >= 4)
        good_rate = int(good_count * 100 / total_count)
        replied_count = sum(1 for f in feedbacks if f.merchant_feedback)
        reply_rate = int(replied_count * 100 / total_count)
    else:
        avg_rating = 0
        good_rate = 0
        reply_rate = 0
    # 评分分布
    rating_dist = {i: 0 for i in range(1, 6)}
    for f in feedbacks:
        r = f.overall_rating
        if r in rating_dist:
            rating_dist[r] += 1
    rating_dist_percent = {k: int(v * 100 / total_count) if total_count else 0 for k, v in rating_dist.items()}
    # 传递到模板
    return render_template('merchant_feedback.html',
        feedbacks=feedbacks,
        avg_rating=avg_rating,
        total_count=total_count,
        good_rate=good_rate,
        reply_rate=reply_rate,
        rating_dist=rating_dist_percent
    )
