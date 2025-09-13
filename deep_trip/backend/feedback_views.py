from flask import Blueprint, jsonify, render_template, request, redirect, url_for, session, flash
from models import db, Feedback, User  # 假设你的模型名为 Feedback, User
import datetime
import json
from sqlalchemy import text  # 导入text函数用于SQL查询

feedback_bp = Blueprint('feedback', __name__)

@feedback_bp.route('/feedback', methods=['GET', 'POST'])
def feedback():
    user = session.get('user')
    if not user:
        flash('请先登录后再评价', 'error')
        return redirect(url_for('user_login'))
    user_id = user.get('id')
    if request.method == 'POST':
        # 从反馈目标中提取商家ID和服务名称
        feedback_target = request.form.get('feedback_target', '')
        # 假设格式为 merchant_id:service_name
        parts = feedback_target.split(':')
        if len(parts) >= 2:
            merchant_id = parts[0]
            service_name = ':'.join(parts[1:])
        else:
            merchant_id = feedback_target
            service_name = request.form.get('service_name', '')
        
        overall_rating = request.form.get('overall_rating', 0)
        environment_rating = request.form.get('environment_rating', 0)
        service_rating = request.form.get('service_rating', 0)
        value_rating = request.form.get('value_rating', 0)
        feedback_content = request.form.get('feedback_content', '')
        
        # 优先获取JSON格式的图片数据
        images_json = request.form.get('images_json', '')
        if not images_json:
            # 兼容旧的提交方式
            images = request.form.getlist('images')
            images_json = json.dumps(images) if images else ''
        
        created_at = datetime.datetime.now()
        
        try:
            # 确保merchant_id是整数类型
            merchant_id = int(merchant_id)
            
            fb = Feedback(
                user_id=user_id,
                merchant_id=merchant_id,
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
            
            # 检查是否是AJAX请求
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return jsonify({'success': True, 'message': '评论提交成功！'})
            
            flash('评论提交成功！', 'success')
        except Exception as e:
            db.session.rollback()
            print(f"提交评论时出错: {e}")
            
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return jsonify({'success': False, 'message': f'提交失败: {str(e)}'})
            
            flash('提交失败，请稍后重试', 'error')
        
        return redirect(url_for('feedback.feedback'))
    
    # GET: 查询当前用户的所有评论
    # 查询当前用户的所有评论
    comments = Feedback.query.filter_by(user_id=user_id).order_by(Feedback.created_at.desc()).all()
    # 查询用户信息
    user_info = User.query.get(user_id)
    
    # 预先解析每个评论中的images JSON字符串
    for comment in comments:
        if comment.images:
            try:
                comment.images_list = json.loads(comment.images)
            except json.JSONDecodeError:
                comment.images_list = []
        else:
            comment.images_list = []
    
    # 查询所有商家和服务项目信息
    service_options = []
    try:
        # 查询shop_info表中的所有记录
        shops = db.session.execute(text('SELECT merchant_id, name, service_items FROM shop_info')).fetchall()
        
        # 处理每个商家的服务项目
        for shop in shops:
            merchant_id = shop.merchant_id
            shop_name = shop.name
            # 解析service_items JSON字符串
            service_items = json.loads(shop.service_items or '[]')
            
            # 为每个服务项目创建一个选项
            for item in service_items:
                if 'name' in item:
                    service_name = item['name']
                    # 格式化为 "merchant_id:商家名称 - 服务名称"
                    option_value = f"{merchant_id}:{shop_name} - {service_name}"
                    service_options.append(option_value)
    except Exception as e:
        print(f"查询商家和服务项目时出错: {e}")
    
    return render_template('feedback.html', comments=comments, user_info=user_info, service_options=service_options)