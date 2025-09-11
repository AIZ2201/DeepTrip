from flask import Blueprint, render_template, session, redirect, url_for, request
from models import db
from sqlalchemy import text
import math

merchant_booking_bp = Blueprint('merchant_booking', __name__)

@merchant_booking_bp.route('/merchant/orders')
def merchant_orders():
    merchant_email = session.get('merchant', {}).get('email')
    if not merchant_email:
        return redirect(url_for('merchant_login'))
    # 获取商家id
    merchant_id = db.session.execute(text('SELECT id FROM user_login WHERE email=:email'), {'email': merchant_email}).scalar()
    # 分页参数
    page = int(request.args.get('page', 1))
    page_size = 10
    # 查询订单总数
    total_orders = db.session.execute(text('SELECT COUNT(*) FROM merchant_order WHERE merchant_id=:mid'), {'mid': merchant_id}).scalar()
    total_pages = max(1, math.ceil(total_orders / page_size))
    # 查询订单列表
    orders_raw = db.session.execute(text('''
        SELECT o.*, u.username FROM merchant_order o LEFT JOIN user_login u ON o.user_id=u.id
        WHERE o.merchant_id=:mid ORDER BY o.order_time DESC LIMIT :offset, :limit
    '''), {'mid': merchant_id, 'offset': (page-1)*page_size, 'limit': page_size}).fetchall()
    # 统计各状态数量
    status_map = {'pending': '待处理', 'confirmed': '已确认', 'completed': '已完成', 'cancelled': '已取消'}
    stats = {}
    for s in status_map:
        stats[s] = db.session.execute(text('SELECT COUNT(*) FROM merchant_order WHERE merchant_id=:mid AND status=:s'), {'mid': merchant_id, 's': s}).scalar()
    # 构造订单数据
    orders = []
    for o in orders_raw:
        orders.append({
            'order_id': o.order_id,
            'username': o.username,
            'product_name': o.product_name,
            'amount': o.amount,
            'status': o.status,
            'status_text': status_map.get(o.status, o.status),
            'order_time': o.order_time.strftime('%Y-%m-%d %H:%M'),
        })
    # 分页范围
    page_range = list(range(1, total_pages+1))
    return render_template('merchant_booking.html',
        orders=orders,
        pending_count=stats['pending'],
        confirmed_count=stats['confirmed'],
        completed_count=stats['completed'],
        cancelled_count=stats['cancelled'],
        current_page=page,
        total_pages=total_pages,
        page_range=page_range
    )
