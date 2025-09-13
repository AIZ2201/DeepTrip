from flask import Blueprint, render_template, session, redirect, url_for, request, jsonify
from models import db, Feedback, User
from sqlalchemy import func, or_
import datetime
import json
from flask import Blueprint, session, redirect, url_for, render_template, request, jsonify

merchant_feedback_bp = Blueprint('merchant_feedback', __name__)

@merchant_feedback_bp.route('/merchant/feedback')
def merchant_feedback():
    merchant = session.get('merchant')
    if not merchant:
        return redirect(url_for('merchant_login'))
    
    # 修复：直接使用merchant_id作为整数类型
    merchant_id = merchant.get('id') if isinstance(merchant, dict) else merchant
    
    # 按照当前商家ID查询反馈
    feedbacks = get_feedbacks_by_merchant(merchant_id)
    
    # 处理 images 字段和 user 信息
    process_feedbacks_data(feedbacks)
    
    # 计算统计信息
    stats = calculate_feedback_stats(feedbacks)
    
    # 传递到模板
    return render_template('merchant_feedback.html',
        feedbacks=feedbacks,
        avg_rating=stats['avg_rating'],
        total_count=stats['total_count'],
        good_rate=stats['good_rate'],
        reply_rate=stats['reply_rate'],
        rating_dist=stats['rating_dist']
    )

# 添加筛选API
@merchant_feedback_bp.route('/merchant/feedback/filter', methods=['POST'])
def filter_feedback():
    merchant = session.get('merchant')
    if not merchant:
        return jsonify({'success': False, 'message': '请先登录'})
    
    merchant_id = merchant.get('id') if isinstance(merchant, dict) else merchant
    
    # 获取筛选参数
    data = request.get_json()
    rating_filter = data.get('rating_filter', 'all')
    reply_status_filter = data.get('reply_status_filter', 'all')
    time_filter = data.get('time_filter', 'all')
    search_term = data.get('search_term', '')
    
    # 构建查询条件
    query = Feedback.query.filter_by(merchant_id=merchant_id)
    
    # 评分筛选
    if rating_filter != 'all':
        if rating_filter == 'negative':  # 差评 (1-2分)
            query = query.filter(Feedback.overall_rating <= 2)
        elif rating_filter == 'positive':  # 好评 (4-5分)
            query = query.filter(Feedback.overall_rating >= 4)
        else:
            query = query.filter(Feedback.overall_rating == int(rating_filter))
    
    # 回复状态筛选
    if reply_status_filter != 'all':
        if reply_status_filter == 'replied':
            query = query.filter(Feedback.merchant_feedback.isnot(None))
        else:  # unreplied
            query = query.filter(Feedback.merchant_feedback.is_(None))
    
    # 时间范围筛选
    now = datetime.datetime.now()
    if time_filter != 'all':
        if time_filter == 'week':
            start_date = now - datetime.timedelta(days=7)
        elif time_filter == 'month':
            start_date = now - datetime.timedelta(days=30)
        elif time_filter == 'quarter':
            start_date = now - datetime.timedelta(days=90)
        elif time_filter == 'half_year':
            start_date = now - datetime.timedelta(days=180)
        elif time_filter == 'year':
            start_date = now - datetime.timedelta(days=365)
        query = query.filter(Feedback.created_at >= start_date)
    
    # 搜索筛选
    if search_term:
        query = query.filter(Feedback.feedback_content.like(f'%{search_term}%'))
    
    # 按时间倒序排序
    feedbacks = query.order_by(Feedback.created_at.desc()).all()
    
    # 处理数据
    process_feedbacks_data(feedbacks)
    
    # 计算统计信息
    stats = calculate_feedback_stats(feedbacks)
    
    # 准备JSON返回数据
    feedbacks_json = []
    for fb in feedbacks:
        feedbacks_json.append({
            'id': fb.id,
            'user': {
                'username': fb.user.username if fb.user else ''
            },
            'feedback_content': fb.feedback_content,
            'overall_rating': fb.overall_rating,
            'service_name': fb.service_name,
            'created_at': fb.created_at.isoformat() if fb.created_at else '',
            'merchant_feedback': fb.merchant_feedback,
            'merchant_reply_time': fb.merchant_reply_time.isoformat() if fb.merchant_reply_time else '',
            'images_list': fb.images_list
        })
    
    return jsonify({
        'success': True,
        'feedbacks': feedbacks_json,
        'stats': stats
    })

# 添加商家回复API
@merchant_feedback_bp.route('/merchant/feedback/reply', methods=['POST'])
def merchant_reply():
    merchant = session.get('merchant')
    if not merchant:
        return jsonify({'success': False, 'message': '请先登录'})
    
    merchant_id = merchant.get('id') if isinstance(merchant, dict) else merchant
    feedback_id = request.form.get('feedback_id')
    reply_content = request.form.get('reply_content')
    
    if not feedback_id or not reply_content:
        return jsonify({'success': False, 'message': '参数错误'})
    
    try:
        # 查询指定的反馈记录
        feedback = Feedback.query.get(feedback_id)
        
        if not feedback or feedback.merchant_id != merchant_id:
            return jsonify({'success': False, 'message': '无权回复该反馈'})
        
        # 更新商家回复
        feedback.merchant_feedback = reply_content
        feedback.merchant_reply_time = datetime.datetime.now()
        
        db.session.commit()
        return jsonify({'success': True, 'message': '回复成功'})
    except Exception as e:
        db.session.rollback()
        print(f'回复反馈时出错: {e}')
        return jsonify({'success': False, 'message': '操作失败，请稍后重试'})

# 辅助函数：根据商家ID获取反馈
def get_feedbacks_by_merchant(merchant_id):
    return Feedback.query.filter_by(merchant_id=merchant_id).order_by(Feedback.created_at.desc()).all()

# 辅助函数：处理反馈数据
def process_feedbacks_data(feedbacks):
    for fb in feedbacks:
        try:
            fb.images_list = json.loads(fb.images) if fb.images else []
        except Exception:
            fb.images_list = []
        fb.user = User.query.get(fb.user_id)
    return feedbacks

# 辅助函数：计算反馈统计信息
def calculate_feedback_stats(feedbacks):
    total_count = len(feedbacks)
    
    if total_count > 0:
        avg_rating = round(sum(f.overall_rating for f in feedbacks) / total_count, 2)
        good_count = sum(1 for f in feedbacks if f.overall_rating >= 4)
        good_rate = int(good_count * 100 / total_count)
        replied_count = sum(1 for f in feedbacks if f.merchant_feedback)
        reply_rate = int(replied_count * 100 / total_count)
        
        # 评分分布
        rating_dist = {i: 0 for i in range(1, 6)}
        for f in feedbacks:
            r = f.overall_rating
            if r in rating_dist:
                rating_dist[r] += 1
        rating_dist_percent = {k: int(v * 100 / total_count) for k, v in rating_dist.items()}
    else:
        avg_rating = 0
        good_rate = 0
        reply_rate = 0
        rating_dist_percent = {i: 0 for i in range(1, 6)}
    
    return {
        'avg_rating': avg_rating,
        'total_count': total_count,
        'good_rate': good_rate,
        'reply_rate': reply_rate,
        'rating_dist': rating_dist_percent
    }