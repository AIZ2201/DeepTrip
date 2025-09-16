from flask import Blueprint, render_template, request, redirect, url_for, flash, session, jsonify
from models import db, Admin, User, Merchant
from admin_login import AdminLogin
from datetime import datetime, timedelta, date
from sqlalchemy import text
import re

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '').strip()
        ###### 测试无法登入的情况 ######
        print(email+" and "+password)
        ##############################
        if not email or not password:
            return jsonify({'success': False, 'message': '邮箱和密码不能为空'})
        if not re.match(r'^[^\s@]+@[^\s@]+\.[^\s@]+$', email):
            return jsonify({'success': False, 'message': '请输入有效的邮箱地址'})
        db_admin = AdminLogin()
        if db_admin.check_admin_login(email, password):
            session.pop('user', None)
            session.pop('merchant', None)
            admin_row = db.session.execute(text('SELECT * FROM admin_login WHERE email=:email'), {'email': email}).fetchone()
            if admin_row:
                session['admin'] = dict(admin_row._mapping)
            else:
                session['admin'] = {'email': email}
            return jsonify({
                'success': True,
                'message': '登录成功',
                'redirect': url_for('admin_dashboard.dashboard')  # 修改这里
            })
        else:
            session['admin'] = None
            return jsonify({'success': False, 'message': '邮箱或密码错误，或账号未激活'})
    return render_template('admin_login.html')

@admin_bp.route('/admin/merchant/review')
def admin_merchant_review():
    return render_template('admin_merchant_review.html')

@admin_bp.route('/admin/data/report')
def admin_data_report():
    # 登录校验
    if 'admin' not in session or not session['admin']:
        return redirect(url_for('admin.admin_login'))
    
    # 查询总用户数
    total_users = db.session.query(User).count()
    # 查询活跃商户数
    active_merchants = db.session.query(Merchant).filter(Merchant.status == 'active').count()
    
    # 查询订单和交易额数据
    today = date.today()
    
    # 获取最近6天的数据（包括今天）
    daily_data = []
    for i in range(5, -1, -1):
        current_date = today - timedelta(days=i)
        date_str = current_date.strftime('%Y-%m-%d')
        
        # 查询当天新增用户数
        # user_login表没有created_at字段，这里改为返回用户总数
        new_users = 0  # 或者可以返回固定值，因为无法区分新增用户
        
        # 查询当天活跃用户数（这里使用订单数作为活跃用户数的代理）
        active_users = db.session.execute(text('SELECT COUNT(DISTINCT user_id) FROM merchant_order WHERE DATE(order_time) = :date'), 
                                        {'date': date_str}).scalar() or 0
        
        # 查询当天新增商户数
        # merchant_login表有created_at字段，可以正常查询
        new_merchants = db.session.execute(text('SELECT COUNT(*) FROM merchant_login WHERE DATE(created_at) = :date'),
                                          {'date': date_str}).scalar() or 0
        
        # 查询当天订单数
        order_count = db.session.execute(text('SELECT COUNT(*) FROM merchant_order WHERE DATE(order_time) = :date'), 
                                        {'date': date_str}).scalar() or 0
        
        # 查询当天交易额
        total_amount = db.session.execute(text('SELECT COALESCE(SUM(amount), 0) FROM merchant_order WHERE DATE(order_time) = :date'), 
                                        {'date': date_str}).scalar() or 0
        
        # 计算平均客单价
        avg_order_value = total_amount / order_count if order_count > 0 else 0
        
        # 计算转化率（这里使用订单用户数/总用户数）
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
    
    # 获取用户增长趋势数据（按周、月、年）
    user_growth = {
        'week': {
            'labels': [],
            'data': []
        },
        'month': {
            'labels': [],
            'data': []
        },
        'year': {
            'labels': [],
            'data': []
        }
    }
    
    # 周数据
    for i in range(6, -1, -1):
        current_date = today - timedelta(days=i)
        day_name = ['周日', '周一', '周二', '周三', '周四', '周五', '周六'][current_date.weekday()]
        date_str = current_date.strftime('%Y-%m-%d')
        
        # user_login表没有created_at字段，这里返回固定值
        day_users = 0
        
        user_growth['week']['labels'].append(day_name)
        user_growth['week']['data'].append(day_users)
    
    # 月数据（最近4周）
    for i in range(3, -1, -1):
        week_start = today - timedelta(days=i*7 + today.weekday())
        week_label = f'第{4-i}周'
        
        # user_login表没有created_at字段，这里返回固定值
        week_users = 0
        
        user_growth['month']['labels'].append(week_label)
        user_growth['month']['data'].append(week_users)
    
    # 年数据（最近12个月）
    for i in range(11, -1, -1):
        month_date = today - timedelta(days=i*30)
        month_str = month_date.strftime('%Y-%m')
        month_label = month_date.strftime('%m月')
        
        # user_login表没有created_at字段，这里返回固定值
        month_users = 0
        
        user_growth['year']['labels'].append(month_label)
        user_growth['year']['data'].append(month_users)
    
    # 按商家类型统计订单数据
    order_type = {
        'labels': [],
        'countData': [],
        'percentageData': []
    }
    
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
    
    # 获取营收趋势数据（按周、月、年）
    revenue_trend = {
        'week': {
            'labels': [],
            'data': []
        },
        'month': {
            'labels': [],
            'data': []
        },
        'year': {
            'labels': [],
            'data': []
        }
    }
    
    # 周营收数据
    for i in range(6, -1, -1):
        current_date = today - timedelta(days=i)
        day_name = ['周日', '周一', '周二', '周三', '周四', '周五', '周六'][current_date.weekday()]
        date_str = current_date.strftime('%Y-%m-%d')
        
        day_revenue = db.session.execute(text('SELECT COALESCE(SUM(amount), 0) FROM merchant_order WHERE DATE(order_time) = :date'), 
                                      {'date': date_str}).scalar() or 0
        
        revenue_trend['week']['labels'].append(day_name)
        revenue_trend['week']['data'].append(day_revenue)
    
    # 月营收数据（最近4周）
    for i in range(3, -1, -1):
        week_start = today - timedelta(days=i*7 + today.weekday())
        week_label = f'第{4-i}周'
        
        week_revenue = db.session.execute(text('SELECT COALESCE(SUM(amount), 0) FROM merchant_order WHERE DATE(order_time) BETWEEN :start_date AND :end_date'), 
                                      {'start_date': week_start.strftime('%Y-%m-%d'),
                                       'end_date': (week_start + timedelta(days=6)).strftime('%Y-%m-%d')}).scalar() or 0
        
        revenue_trend['month']['labels'].append(week_label)
        revenue_trend['month']['data'].append(week_revenue)
    
    # 获取地区分布数据
    region_distribution = {
        'users': {
            'labels': [],
            'data': []
        },
        'merchants': {
            'labels': [],
            'data': []
        },
        'orders': {
            'labels': [],
            'data': []
        }
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
    
    # 处理前6个地区的数据
    for row in region_data:
        region_distribution['users']['labels'].append(row.city or '未知')
        region_distribution['users']['data'].append(row.user_count)
        region_distribution['merchants']['labels'].append(row.city or '未知')
        region_distribution['merchants']['data'].append(row.merchant_count)
        region_distribution['orders']['labels'].append(row.city or '未知')
        region_distribution['orders']['data'].append(row.order_count)
    
    # 添加其他地区
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
    
    # 转换为JSON字符串
    import json
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
    
# 处理动态报表生成请求
@admin_bp.route('/admin/data_report', methods=['POST'])
def data_report_post():
    if 'admin' not in session or not session['admin']:
        return jsonify({'success': False, 'message': '请先登录'})
    
    try:
        data = request.json
        report_type = data.get('report_type', 'overview')
        time_range = data.get('time_range', 'week')
        
        # 根据报表类型和时间范围查询数据
        result = {
            'user_growth': {},
            'order_type': {},
            'revenue_trend': {},
            'region_distribution': {}
        }
        
        today = date.today()
        
        # 用户增长数据
        user_growth = {
            'week': {
                'labels': [],
                'data': []
            },
            'month': {
                'labels': [],
                'data': []
            },
            'year': {
                'labels': [],
                'data': []
            }
        }
        
        # 填充用户增长数据（与GET请求中的逻辑类似）
        # ...
        
        # 订单类型数据
        order_type = {
            'labels': [],
            'countData': [],
            'percentageData': []
        }
        
        # 营收趋势数据
        revenue_trend = {
            'week': {
                'labels': [],
                'data': []
            },
            'month': {
                'labels': [],
                'data': []
            },
            'year': {
                'labels': [],
                'data': []
            }
        }
        
        # 地区分布数据
        region_distribution = {
            'users': {
                'labels': [],
                'data': []
            },
            'merchants': {
                'labels': [],
                'data': []
            },
            'orders': {
                'labels': [],
                'data': []
            }
        }
        
        # 根据报表类型返回相应的数据
        if report_type == 'users':
            result['user_growth'] = user_growth
            result['region_distribution'] = region_distribution
        elif report_type == 'orders':
            result['order_type'] = order_type
            result['revenue_trend'] = revenue_trend
        elif report_type == 'revenue':
            result['revenue_trend'] = revenue_trend
        else:
            # 概览报表返回所有数据
            result['user_growth'] = user_growth
            result['order_type'] = order_type
            result['revenue_trend'] = revenue_trend
            result['region_distribution'] = region_distribution
        
        return jsonify(result)
    except Exception as e:
        print(f'Error generating report: {e}')
        return jsonify({'success': False, 'message': '生成报表失败'})

@admin_bp.route('/admin/export/excel', methods=['GET'])
def export_excel():
    from io import BytesIO
    import pandas as pd
    from flask import send_file
    
    # 登录校验
    if 'admin' not in session or not session['admin']:
        return redirect(url_for('admin.admin_login'))
    
    # 查询数据
    today = date.today()
    daily_data = []
    
    for i in range(30, -1, -1):  # 导出最近30天的数据
        current_date = today - timedelta(days=i)
        date_str = current_date.strftime('%Y-%m-%d')
        
        # user_login表没有created_at字段，这里返回固定值
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
        total_users = db.session.query(User).count()
        conversion_rate = (active_users / total_users * 100) if total_users > 0 else 0
        
        daily_data.append({
            '日期': date_str,
            '新增用户': new_users,
            '活跃用户': active_users,
            '新增商户': new_merchants,
            '订单数': order_count,
            '交易额(元)': total_amount,
            '平均客单价(元)': round(avg_order_value, 2),
            '转化率(%)': round(conversion_rate, 2)
        })
    
    # 创建DataFrame
    df = pd.DataFrame(daily_data)
    
    # 创建BytesIO对象
    output = BytesIO()
    
    # 创建Excel写入器
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='数据报表')
    
    # 定位到文件开头
    output.seek(0)
    
    # 发送文件
    return send_file(output, download_name='data_report.xlsx', as_attachment=True, mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')