# 在文件顶部添加缺失的导入
from flask import Blueprint, render_template, request, redirect, url_for, session
from .models import db
from sqlalchemy import text
import math
from datetime import datetime, timedelta

merchant_booking_bp = Blueprint('merchant_booking', __name__)

@merchant_booking_bp.route('/merchant/orders')
def merchant_orders():
    merchant_email = session.get('merchant', {}).get('email')
    if not merchant_email:
        return redirect(url_for('merchant.merchant_login'))
    
    # 获取商家id
    merchant_id = db.session.execute(text('SELECT id FROM merchant_login WHERE email=:email'), {'email': merchant_email}).scalar()
    
    # 添加自动完成订单的逻辑
    # 查找所有状态为confirmed且服务结束时间已超过3小时的订单
    try:
        # 计算当前时间减去3小时
        three_hours_ago = datetime.now() - timedelta(hours=1)
        
        # 查询并更新符合条件的订单
        db.session.execute(text('''
            UPDATE orders 
            SET status = 'completed' 
            WHERE merchant_id = :merchant_id 
            AND status = 'confirmed' 
            AND service_end_time <= :three_hours_ago
        '''), {'merchant_id': merchant_id, 'three_hours_ago': three_hours_ago})
        db.session.commit()
        
        # 记录更新的订单数量（可选）
        updated_count = db.session.execute(text('''
            SELECT ROW_COUNT()
        '''))
        print(f"自动完成了 {updated_count.scalar()} 个订单")
        
    except Exception as e:
        db.session.rollback()
        print(f"自动完成订单时发生错误: {str(e)}")
    
    # 分页参数
    page = int(request.args.get('page', 1))
    page_size = 10
    
    # 查询orders表中属于当前商家的订单总数
    total_orders = db.session.execute(text('''
        SELECT COUNT(*) FROM orders 
        WHERE merchant_id = :merchant_id
    '''), {'merchant_id': merchant_id}).scalar()
    
    print(f"Total orders for merchant {merchant_id}: {total_orders}")
    
    # 在第37行左右（total_pages 变量定义后）添加以下代码：
    total_pages = max(1, math.ceil(total_orders / page_size))
    
    # 添加这三行代码来计算 page_range
    start_page = max(1, page - 2)
    end_page = min(total_pages, start_page + 4)
    page_range = range(start_page, end_page + 1)
    
    # 原来的代码继续：
    # 查询订单列表（关联用户表获取用户名）
    orders_raw = db.session.execute(text('''
        SELECT 
            o.id as order_id,
            o.service_name as product_name,
            o.price as amount,
            o.status,
            o.book_time as order_time,
            u.username
        FROM orders o
        LEFT JOIN user_login u ON o.user_id = u.id
        WHERE o.merchant_id = :merchant_id
        ORDER BY o.book_time DESC 
        LIMIT :offset, :limit
    '''), {
        'merchant_id': merchant_id, 
        'offset': (page-1)*page_size, 
        'limit': page_size
    }).fetchall()
    
    # 统计各状态订单数量
    status_counts = {'pending': 0, 'confirmed': 0, 'completed': 0, 'cancelled': 0}
    status_map = {'pending': '待处理', 'confirmed': '已确认', 'completed': '已完成', 'cancelled': '已取消'}
    
    for status in status_map.keys():
        try:
            count = db.session.execute(text('''
                SELECT COUNT(*) FROM orders 
                WHERE merchant_id = :merchant_id AND status = :status
            '''), {'merchant_id': merchant_id, 'status': status}).scalar()
            status_counts[status] = count or 0  # 确保即使为None也显示为0
            print(f"{status} orders count: {status_counts[status]}")
        except Exception as e:
            print(f"Error counting {status} orders: {str(e)}")
    
    # 构造订单数据
    orders = []
    for o in orders_raw:
        orders.append({
            'order_id': o.order_id,
            'username': o.username or '未知用户',
            'product_name': o.product_name or '未知产品',
            'amount': o.amount or 0,
            'status': o.status or 'unknown',
            'status_text': status_map.get(o.status, '未知状态'),
            'order_time': o.order_time.strftime('%Y-%m-%d %H:%M') if o.order_time else '未知时间',
        })
    
    print(f"Orders data sent to template: {len(orders)} items")
    
    # 分页范围    
    return render_template('merchant_booking.html',
        orders=orders,
        pending_count=status_counts['pending'],
        confirmed_count=status_counts['confirmed'],
        completed_count=status_counts['completed'],
        cancelled_count=status_counts['cancelled'],
        current_page=page,
        total_pages=total_pages,
        page_range=page_range,
        debug_info={
            'merchant_id': merchant_id,
            'merchant_email': merchant_email
        }
    )

# 在文件末尾添加处理订单状态更新的路由
@merchant_booking_bp.route('/merchant/orders/update_status', methods=['POST'])
def update_order_status():
    merchant_email = session.get('merchant', {}).get('email')
    if not merchant_email:
        return {'success': False, 'message': '请先登录'}
    
    # 获取商家id
    merchant_id = db.session.execute(text('SELECT id FROM merchant_login WHERE email=:email'), {'email': merchant_email}).scalar()
    
    # 获取请求参数
    order_id = request.json.get('order_id')
    action = request.json.get('action')  # 'confirm_refund' 或 'reject_refund'
    
    if not order_id or not action:
        return {'success': False, 'message': '参数错误'}
    
    # 验证订单是否属于该商家
    order = db.session.execute(text('''
        SELECT * FROM orders 
        WHERE id = :order_id AND merchant_id = :merchant_id
    '''), {'order_id': order_id, 'merchant_id': merchant_id}).fetchone()
    
    if not order:
        return {'success': False, 'message': '订单不存在或不属于当前商家'}
    
    # 检查订单当前状态是否为pending（退款申请状态）
    if order.status != 'pending':
        return {'success': False, 'message': '该订单状态不支持此操作'}
    
    # 根据操作更新订单状态
    try:
        new_status = 'cancelled' if action == 'confirm_refund' else 'completed'
        db.session.execute(text('''
            UPDATE orders 
            SET status = :new_status 
            WHERE id = :order_id
        '''), {'new_status': new_status, 'order_id': order_id})
        db.session.commit()
        return {'success': True, 'message': '操作成功', 'new_status': new_status}
    except Exception as e:
        db.session.rollback()
        print(f"Error updating order status: {str(e)}")
        return {'success': False, 'message': '操作失败，请重试'}