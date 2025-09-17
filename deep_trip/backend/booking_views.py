# 完整修改后的booking_views.py
from flask import Blueprint, render_template, request, jsonify, session
from .models import db
from sqlalchemy import text, func
import json
import re
from datetime import datetime

booking_bp = Blueprint('booking', __name__)

@booking_bp.route('/booking')
def booking():
    # 查询shop_info表中的所有商家信息
    shops = db.session.execute(text('''
        SELECT 
            si.id,
            si.merchant_id,
            si.name as merchant_name,
            si.description,
            si.address,
            si.city,
            si.district,
            si.category,
            si.price_range,
            si.images,
            si.service_items
        FROM shop_info si
        ORDER BY si.category, si.name
    ''')).fetchall()
    
    # 获取所有反馈信息（一次性查询提高效率）
    all_feedbacks = db.session.execute(text('''
        SELECT 
            service_name,
            overall_rating
        FROM feedback 
        WHERE service_name IS NOT NULL
    ''')).fetchall()
    
    # 按类别分组商家信息
    hotels = []
    attractions = []
    restaurants = []
    
    # 创建商家服务项目映射
    merchant_services = {}
    
    for shop in shops:
        shop_dict = dict(shop._mapping)
        
        # 处理图片数据
        images = []
        if shop_dict.get('images'):
            try:
                images = json.loads(shop_dict['images'])
            except:
                images = []
        shop_dict['images'] = images
        
        # 处理service_items数据
        service_items = []
        if shop_dict.get('service_items'):
            try:
                service_items = json.loads(shop_dict['service_items'])
            except:
                service_items = []
        shop_dict['service_items'] = service_items
        
        # 将服务项目存储到映射中
        merchant_services[shop_dict['merchant_name']] = service_items
        
        # 统计该店铺的所有评分（遍历所有反馈）
        shop_ratings = []
        shop_review_count = 0
        
        for fb in all_feedbacks:
            if fb.service_name and shop_dict['merchant_name'] in fb.service_name:
                # 提取店铺名（服务名称中" - "前的部分）
                if ' - ' in fb.service_name:
                    merchant_name = fb.service_name.split(' - ')[0].strip()
                else:
                    merchant_name = fb.service_name.strip()
                
                # 只计算与当前店铺名完全匹配的评分
                if merchant_name == shop_dict['merchant_name']:
                    shop_ratings.append(fb.overall_rating)
                    shop_review_count += 1
        
        # 计算平均评分
        if shop_ratings:
            overall_avg_rating = sum(shop_ratings) / len(shop_ratings)
        else:
            overall_avg_rating = 0
        
        shop_dict['avg_rating'] = overall_avg_rating
        shop_dict['review_count'] = shop_review_count
        
        # 按类别分组
        if shop_dict['category'] == 'hotel':
            hotels.append(shop_dict)
        elif shop_dict['category'] == 'attraction':
            attractions.append(shop_dict)
        elif shop_dict['category'] == 'restaurant':
            restaurants.append(shop_dict)
    
    return render_template('booking.html', 
                         hotels=hotels, 
                         attractions=attractions, 
                         restaurants=restaurants,
                         merchant_services=merchant_services)

@booking_bp.route('/submit_booking', methods=['POST'])
def submit_booking():
    try:
        print("=== 开始处理预订请求 ===")
        data = request.get_json()
        print(f"请求数据: {data}")
        
        # 获取表单数据
        merchant_id = data.get('merchant_id')
        category = data.get('category')
        service_name = data.get('service_name')
        service_start_time_str = data.get('service_start_time')  # 获取时间字符串
        service_end_time_str = data.get('service_end_time')      # 获取时间字符串
        customer_name = data.get('customer_name')
        phonenumber = data.get('phonenumber')
        price = data.get('price')
        
        # 获取当前用户ID
        user_info = session.get('user')
        if not user_info:
            print("用户未登录")
            return jsonify({'success': False, 'message': '请先登录'}), 401
        
        user_id = user_info.get('id')
        
        # 转换时间字符串为datetime对象 - 处理前导空格和缺少日期的情况
        try:
            from datetime import date
            
            # 去除前导空格
            service_start_time_str = service_start_time_str.strip()
            service_end_time_str = service_end_time_str.strip()
            
            # 直接转换时间字符串，不再自动添加日期
            service_start_time = datetime.strptime(service_start_time_str, '%Y-%m-%d %H:%M:%S')
            service_end_time = datetime.strptime(service_end_time_str, '%Y-%m-%d %H:%M:%S')
        except (ValueError, TypeError) as e:
            print(f"时间格式转换错误: {e}")
            return jsonify({'success': False, 'message': '时间格式不正确，请使用YYYY-MM-DD HH:MM:SS格式'}), 400
        
        # 对于酒店预订，重新计算价格（根据入住天数）
        if category == 'hotel':
            # 计算入住天数
            time_diff = service_end_time - service_start_time
            days_diff = time_diff.days + 1
            
            # 重新计算总价格 = 单天价格 × 入住天数
            # 注意：这里假设前端传来的price是单天价格
            original_price = float(price) if price else 0
            final_price = original_price * days_diff
            price = final_price  # 更新为最终价格
            print(f"酒店价格重新计算: {original_price} × {days_diff}天 = {final_price}")
        
        # 获取当前时间作为预订时间
        book_time = datetime.now()

        # 插入订单到orders表（包含book_time字段）
        result = db.session.execute(text('''
            INSERT INTO orders (user_id, merchant_id, category, service_name, 
                              service_start_time, service_end_time, customer_name, 
                              phonenumber, price, status, book_time)
            VALUES (:user_id, :merchant_id, :category, :service_name, 
                   :service_start_time, :service_end_time, :customer_name, 
                   :phonenumber, :price, 'confirmed', :book_time)
        '''), {
            'user_id': user_id,
            'merchant_id': merchant_id,
            'category': category,
            'service_name': service_name,
            'service_start_time': service_start_time,
            'service_end_time': service_end_time,
            'customer_name': customer_name,
            'phonenumber': phonenumber,
            'price': price,
            'book_time': book_time
        })
        
        db.session.commit()
        return jsonify({'success': True, 'message': '预订提交成功！'})
        
    except Exception as e:
        print(f"发生异常: {str(e)}")
        import traceback
        print(f"详细堆栈信息: {traceback.format_exc()}")
        db.session.rollback()
        return jsonify({'success': False, 'message': f'预订失败：{str(e)}'}), 500
    
    
@booking_bp.route('/user_orders')
def get_user_orders():
    try:
        # 检查用户是否登录
        user_info = session.get('user')
        if not user_info:
            return jsonify({'success': False, 'message': '请先登录'}), 401
        
        user_id = user_info.get('id')
        
        # 查询当前用户的所有订单
        orders = db.session.execute(text('''
            SELECT 
                o.id,
                o.merchant_id,
                o.category,
                o.service_name,
                o.service_start_time,
                o.service_end_time,
                o.customer_name,
                o.phonenumber,
                o.price,
                o.status,
                o.book_time,
                si.name as merchant_name
            FROM orders o
            LEFT JOIN shop_info si ON o.merchant_id = si.merchant_id
            WHERE o.user_id = :user_id
            ORDER BY o.book_time DESC
        '''), {'user_id': user_id}).fetchall()
        
        # 格式化订单数据
        orders_list = []
        for order in orders:
            order_dict = dict(order._mapping)
            # 转换datetime对象为字符串
            for time_field in ['service_start_time', 'service_end_time', 'book_time']:
                if order_dict.get(time_field):
                    order_dict[time_field] = order_dict[time_field].strftime('%Y-%m-%d %H:%M:%S')
            orders_list.append(order_dict)
        
        return jsonify({'success': True, 'orders': orders_list})
        
    except Exception as e:
        print(f"获取用户订单失败: {str(e)}")
        return jsonify({'success': False, 'message': '获取订单失败'}), 500

@booking_bp.route('/cancel_order', methods=['POST'])
def cancel_order():
    try:
        # 检查用户是否登录
        user_info = session.get('user')
        if not user_info:
            return jsonify({'success': False, 'message': '请先登录'}), 401
        
        user_id = user_info.get('id')
        data = request.get_json()
        order_id = data.get('order_id')
        
        # 验证订单属于当前用户
        order = db.session.execute(text('''
            SELECT id FROM orders 
            WHERE id = :order_id AND user_id = :user_id
        '''), {'order_id': order_id, 'user_id': user_id}).fetchone()
        
        if not order:
            return jsonify({'success': False, 'message': '订单不存在或无权操作'}), 403
        
        # 更新订单状态为pending（申请退订中）
        db.session.execute(text('''
            UPDATE orders SET status = 'pending' 
            WHERE id = :order_id
        '''), {'order_id': order_id})
        
        db.session.commit()
        return jsonify({'success': True, 'message': '退订申请已提交，等待处理'})
        
    except Exception as e:
        print(f"退订申请失败: {str(e)}")
        db.session.rollback()
        return jsonify({'success': False, 'message': '退订申请失败'}), 500