from flask import Blueprint, render_template, request, session, redirect, url_for, jsonify
from models import db
from sqlalchemy import text
import json

merchant_info_bp = Blueprint('merchant_info', __name__)

@merchant_info_bp.route('/merchant/info', methods=['GET', 'POST'])
def merchant_info():
    merchant_email = session.get('merchant', {}).get('email')
    if not merchant_email:
        return redirect(url_for('merchant_login'))
    # 查询店铺信息
    shop = db.session.execute(text('SELECT * FROM shop_info WHERE merchant_id=(SELECT id FROM user_login WHERE email=:email)'), {'email': merchant_email}).fetchone()
    if request.method == 'POST':
        data = request.get_json()
        # 只允许上传一次，已存在则拒绝
        if shop:
            return jsonify({'success': False, 'message': '您已上传过店铺信息，如需修改请联系管理员'})
        # 解析数据
        basic = data.get('basicInfo', {})
        location = data.get('locationInfo', {})
        contact = data.get('contactInfo', {})
        business_hours = json.dumps(data.get('businessHours', []), ensure_ascii=False)
        service_items = json.dumps(data.get('serviceItems', []), ensure_ascii=False)
        holiday_info = data.get('holidayInfo', '')
        images = json.dumps(data.get('images', []), ensure_ascii=False) if 'images' in data else ''
        merchant_id = db.session.execute(text('SELECT id FROM user_login WHERE email=:email'), {'email': merchant_email}).scalar()
        db.session.execute(text('''
            INSERT INTO shop_info (merchant_id, name, category, price_range, description, address, city, district, phone, email, website, wechat, holiday_info, images, business_hours, service_items)
            VALUES (:merchant_id, :name, :category, :price_range, :description, :address, :city, :district, :phone, :email, :website, :wechat, :holiday_info, :images, :business_hours, :service_items)
        '''), {
            'merchant_id': merchant_id,
            'name': basic.get('name',''),
            'category': basic.get('category',''),
            'price_range': basic.get('priceRange',''),
            'description': basic.get('description',''),
            'address': location.get('address',''),
            'city': location.get('city',''),
            'district': location.get('district',''),
            'phone': contact.get('phone',''),
            'email': contact.get('email',''),
            'website': contact.get('website',''),
            'wechat': contact.get('wechat',''),
            'holiday_info': holiday_info,
            'images': images,
            'business_hours': business_hours,
            'service_items': service_items
        })
        db.session.commit()
        return jsonify({'success': True, 'message': '店铺信息已保存'})
    # GET请求：已填则展示，未填则进入上传页
    if shop:
        # 转为dict
        shop_dict = dict(shop)
        # 解析json字段
        shop_dict['business_hours'] = json.loads(shop_dict.get('business_hours','[]'))
        shop_dict['service_items'] = json.loads(shop_dict.get('service_items','[]'))
        shop_dict['images'] = json.loads(shop_dict.get('images','[]'))
        return render_template('merchant_info_upload.html', shop_info=shop_dict, filled=True)
    else:
        return render_template('merchant_info_upload.html', shop_info=None, filled=False)
