from flask import Blueprint, render_template, request, redirect, url_for, session, jsonify
from .models import db, User, Merchant
from datetime import datetime, timedelta, date
from sqlalchemy import text
import json

admin_data_report_bp = Blueprint('admin_data_report', __name__)

@admin_data_report_bp.route('/admin/data/report')
def admin_data_report():
    # 登录校验
    if 'admin' not in session or not session['admin']:
        return redirect(url_for('admin.admin_login'))
    
    # 查询总用户数
    total_users = db.session.query(User).count()
    # 查询活跃商户数
    active_merchants = db.session.query(Merchant).filter(Merchant.status == 'active').count()
    
    today = date.today()
    daily_data = []
    for i in range(5, -1, -1):
        current_date = today - timedelta(days=i)
        date_str = current_date.strftime('%Y-%m-%d')
        new_users = 0
        active_users = db.session.execute(text('SELECT COUNT(DISTINCT user_id) FROM merchant_order WHERE DATE(order_time) = :date'), 
                                        {'date': date_str}).scalar() or 0
        new_merchants = db.session.execute(text('SELECT COUNT(*) FROM merchant_login WHERE DATE(created_at) = :date'),
                                          {'date': date_str}).scalar() or 0
        order_count = db.session.execute(text('SELECT COUNT(*) FROM merchant_order WHERE DATE(order_time) = :date'), 
                                        {'date': date_str}).scalar() or 0
        total_amount = db.session.execute(text('SELECT COALESCE(SUM(amount), 0) FROM merchant_order WHERE DATE(order_time) = :date'), 
                                        {'date': date_str}).scalar() or 0
        avg_order_value = total_amount / order_count if order_count > 0 else 0
        conversion_rate = (active_users / total_users * 100) if total_users > 0 else 0
        daily_data.append({
            'date': date_str,
            'new_users': new_users,
            'active_users': active_users,
            'new_merchants': new_merchants,
            'order_count': order_count,
            'total_amount': total_amount,
            'avg_order_value': round(avg_order_value, 2),
            'conversion_rate': round(conversion_rate, 2)
        })
    user_growth = {
        'week': {'labels': [], 'data': []},
        'month': {'labels': [], 'data': []},
        'year': {'labels': [], 'data': []}
    }
    for i in range(6, -1, -1):
        current_date = today - timedelta(days=i)
        day_name = ['周日', '周一', '周二', '周三', '周四', '周五', '周六'][current_date.weekday()]
        user_growth['week']['labels'].append(day_name)
        user_growth['week']['data'].append(0)
    for i in range(3, -1, -1):
        week_label = f'第{4-i}周'
        user_growth['month']['labels'].append(week_label)
        user_growth['month']['data'].append(0)
    for i in range(11, -1, -1):
        month_date = today - timedelta(days=i*30)
        month_label = month_date.strftime('%m月')
        user_growth['year']['labels'].append(month_label)
        user_growth['year']['data'].append(0)
    order_type = {'labels': [], 'countData': [], 'percentageData': []}
    order_type_data = db.session.execute(text('''
        SELECT m.business_type, COUNT(o.id) as order_count, SUM(o.amount) as total_amount
        FROM merchant_order o
        JOIN merchant_login m ON o.merchant_id = m.id
        GROUP BY m.business_type
    ''')).fetchall()
    total_orders = sum(row.order_count for row in order_type_data)
    for row in order_type_data:
        order_type['labels'].append(row.business_type)
        order_type['countData'].append(row.order_count)
        order_type['percentageData'].append(round(row.order_count / total_orders * 100, 2) if total_orders > 0 else 0)
    revenue_trend = {
        'week': {'labels': [], 'data': []},
        'month': {'labels': [], 'data': []},
        'year': {'labels': [], 'data': []}
    }
    for i in range(6, -1, -1):
        current_date = today - timedelta(days=i)
        day_name = ['周日', '周一', '周二', '周三', '周四', '周五', '周六'][current_date.weekday()]
        day_revenue = db.session.execute(text('SELECT COALESCE(SUM(amount), 0) FROM merchant_order WHERE DATE(order_time) = :date'), 
                                      {'date': current_date.strftime('%Y-%m-%d')}).scalar() or 0
        revenue_trend['week']['labels'].append(day_name)
        revenue_trend['week']['data'].append(day_revenue)
    for i in range(3, -1, -1):
        week_start = today - timedelta(days=i*7 + today.weekday())
        week_label = f'第{4-i}周'
        week_revenue = db.session.execute(text('SELECT COALESCE(SUM(amount), 0) FROM merchant_order WHERE DATE(order_time) BETWEEN :start_date AND :end_date'), 
                                      {'start_date': week_start.strftime('%Y-%m-%d'),
                                       'end_date': (week_start + timedelta(days=6)).strftime('%Y-%m-%d')}).scalar() or 0
        revenue_trend['month']['labels'].append(week_label)
        revenue_trend['month']['data'].append(week_revenue)
    region_distribution = {
        'users': {'labels': [], 'data': []},
        'merchants': {'labels': [], 'data': []},
        'orders': {'labels': [], 'data': []}
    }
    region_data = db.session.execute(text('''
        SELECT s.city, COUNT(DISTINCT u.id) as user_count, COUNT(DISTINCT m.id) as merchant_count, COUNT(o.id) as order_count
        FROM user_login u
        LEFT JOIN merchant_order o ON u.id = o.user_id
        LEFT JOIN merchant_login m ON o.merchant_id = m.id
        LEFT JOIN shop_info s ON m.id = s.merchant_id
        GROUP BY s.city
        ORDER BY user_count DESC
        LIMIT 6
    ''')).fetchall()
    other_users = 0
    other_merchants = 0
    other_orders = 0
    for row in region_data:
        region_distribution['users']['labels'].append(row.city or '未知')
        region_distribution['users']['data'].append(row.user_count)
        region_distribution['merchants']['labels'].append(row.city or '未知')
        region_distribution['merchants']['data'].append(row.merchant_count)
        region_distribution['orders']['labels'].append(row.city or '未知')
        region_distribution['orders']['data'].append(row.order_count)
    total_user_count = db.session.query(User).count()
    other_users = total_user_count - sum(region_distribution['users']['data'])
    other_merchants = active_merchants - sum(region_distribution['merchants']['data'])
    total_order_count = db.session.execute(text('SELECT COUNT(*) FROM merchant_order')).scalar() or 0
    other_orders = total_order_count - sum(region_distribution['orders']['data'])
    if other_users > 0 or other_merchants > 0 or other_orders > 0:
        region_distribution['users']['labels'].append('其他')
        region_distribution['users']['data'].append(other_users)
        region_distribution['merchants']['labels'].append('其他')
        region_distribution['merchants']['data'].append(other_merchants)
        region_distribution['orders']['labels'].append('其他')
        region_distribution['orders']['data'].append(other_orders)
    user_growth_json = json.dumps(user_growth, ensure_ascii=False)
    order_type_json = json.dumps(order_type, ensure_ascii=False)
    revenue_trend_json = json.dumps(revenue_trend, ensure_ascii=False)
    region_distribution_json = json.dumps(region_distribution, ensure_ascii=False)
    return render_template('admin_data_report.html',
        total_users=total_users,
        active_merchants=active_merchants,
        daily_data=daily_data,
        user_growth_json=user_growth_json,
        order_type_json=order_type_json,
        revenue_trend_json=revenue_trend_json,
        region_distribution_json=region_distribution_json
    )

@admin_data_report_bp.route('/admin/data_report', methods=['POST'])
def data_report_post():
    if 'admin' not in session or not session['admin']:
        return jsonify({'success': False, 'message': '请先登录'})
    try:
        data = request.json
        report_type = data.get('report_type', 'overview')
        time_range = data.get('time_range', 'week')
        result = {
            'user_growth': {},
            'order_type': {},
            'revenue_trend': {},
            'region_distribution': {}
        }
        today = date.today()
        user_growth = {
            'week': {'labels': [], 'data': []},
            'month': {'labels': [], 'data': []},
            'year': {'labels': [], 'data': []}
        }
        for i in range(6, -1, -1):
            current_date = today - timedelta(days=i)
            day_name = ['周日', '周一', '周二', '周三', '周四', '周五', '周六'][current_date.weekday()]
            user_growth['week']['labels'].append(day_name)
            user_growth['week']['data'].append(0)
        for i in range(3, -1, -1):
            week_label = f'第{4-i}周'
            user_growth['month']['labels'].append(week_label)
            user_growth['month']['data'].append(0)
        for i in range(11, -1, -1):
            month_date = today - timedelta(days=i*30)
            month_label = month_date.strftime('%m月')
            user_growth['year']['labels'].append(month_label)
            user_growth['year']['data'].append(0)
        order_type = {'labels': [], 'countData': [], 'percentageData': []}
        revenue_trend = {
            'week': {'labels': [], 'data': []},
            'month': {'labels': [], 'data': []},
            'year': {'labels': [], 'data': []}
        }
        region_distribution = {
            'users': {'labels': [], 'data': []},
            'merchants': {'labels': [], 'data': []},
            'orders': {'labels': [], 'data': []}
        }
        if report_type == 'users':
            result['user_growth'] = user_growth
            result['region_distribution'] = region_distribution
        elif report_type == 'orders':
            result['order_type'] = order_type
            result['revenue_trend'] = revenue_trend
        elif report_type == 'revenue':
            result['revenue_trend'] = revenue_trend
        else:
            result['user_growth'] = user_growth
            result['order_type'] = order_type
            result['revenue_trend'] = revenue_trend
            result['region_distribution'] = region_distribution
        return jsonify(result)
    except Exception as e:
        print(f'Error generating report: {e}')
        return jsonify({'success': False, 'message': '生成报表失败'})
