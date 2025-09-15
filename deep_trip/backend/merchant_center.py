from flask import Blueprint, render_template, request, session, redirect, url_for, flash, jsonify
from models import db
from sqlalchemy import text
import json

merchant_center_bp = Blueprint('merchant_center', __name__)

@merchant_center_bp.route('/merchant/center', methods=['GET'])
def center():
    merchant = session.get('merchant', {})
    merchant_id = merchant.get('id')
    if not merchant_id:
        return redirect(url_for('merchant.merchant_login'))
    # 查询账号信息
    merchant_row = db.session.execute(
        text('SELECT * FROM merchant_login WHERE id=:id'),
        {'id': merchant_id}
    ).fetchone()
    merchant_info = dict(merchant_row._mapping) if merchant_row else {}
    # 查询店铺信息
    shop_row = db.session.execute(
        text('SELECT * FROM shop_info WHERE merchant_id=:merchant_id'),
        {'merchant_id': merchant_id}
    ).fetchone()
    shop_info = None
    if shop_row:
        shop_info = dict(shop_row._mapping)
        for k in ['name','category','price_range','description','address','city','district','phone','email','website','wechat','holiday_info']:
            if k not in shop_info or shop_info[k] is None:
                shop_info[k] = ''
        shop_info['business_hours'] = json.loads(shop_info.get('business_hours','[]'))
        shop_info['service_items'] = json.loads(shop_info.get('service_items','[]'))
        images_raw = shop_info.get('images', '[]')
        if not images_raw or images_raw.strip() in ['', 'null', 'None']:
            shop_info['images'] = []
        else:
            shop_info['images'] = json.loads(images_raw)
    return render_template('merchant_center.html', merchant=merchant_info, shop_info=shop_info)

@merchant_center_bp.route('/merchant/center/edit', methods=['POST'])
def edit_account():
    merchant = session.get('merchant', {})
    merchant_id = merchant.get('id')
    if not merchant_id:
        return redirect(url_for('merchant.merchant_login'))
    username = request.form.get('username', '').strip()
    password = request.form.get('password', '').strip()
    # 简单校验
    if not username and not password:
        flash('请输入要修改的用户名或密码', 'error')
        return redirect(url_for('merchant_center.center'))
    # 检查用户名唯一性
    if username:
        exists = db.session.execute(
            text('SELECT id FROM merchant_login WHERE username=:username AND id!=:id'),
            {'username': username, 'id': merchant_id}
        ).fetchone()
        if exists:
            flash('用户名已被占用', 'error')
            return redirect(url_for('merchant_center.center'))
        db.session.execute(
            text('UPDATE merchant_login SET username=:username WHERE id=:id'),
            {'username': username, 'id': merchant_id}
        )
        session['merchant']['username'] = username
    # 修改密码
    if password:
        db.session.execute(
            text('UPDATE merchant_login SET password=:password WHERE id=:id'),
            {'password': password, 'id': merchant_id}
        )
    db.session.commit()
    flash('修改成功', 'success')
    return redirect(url_for('merchant_center.center'))

@merchant_center_bp.route('/merchant/center/edit_field', methods=['POST'])
def edit_account_field():
    merchant = session.get('merchant', {})
    merchant_id = merchant.get('id')
    if not merchant_id:
        return jsonify({'success': False, 'message': '未登录'})
    data = request.get_json()
    field = data.get('field')
    value = data.get('value', '').strip()
    allowed_fields = ['username', 'name', 'email', 'phone', 'business_type', 'password']
    if field not in allowed_fields:
        return jsonify({'success': False, 'message': '不允许修改该项'})
    # 校验唯一性
    if field in ['username', 'email', 'phone']:
        exists = db.session.execute(
            text(f'SELECT id FROM merchant_login WHERE {field}=:value AND id!=:id'),
            {'value': value, 'id': merchant_id}
        ).fetchone()
        if exists:
            return jsonify({'success': False, 'message': f'{field}已被占用'})
    # 更新
    db.session.execute(
        text(f'UPDATE merchant_login SET {field}=:value WHERE id=:id'),
        {'value': value, 'id': merchant_id}
    )
    db.session.commit()
    # 更新session
    session['merchant'][field] = value
    return jsonify({'success': True})
