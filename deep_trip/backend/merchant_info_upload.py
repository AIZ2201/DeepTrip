from flask import Blueprint, render_template, request, session, redirect, url_for, jsonify
from models import db
from sqlalchemy import text
import json

merchant_info_bp = Blueprint('merchant_info', __name__)

@merchant_info_bp.route('/merchant/info', methods=['GET', 'POST'])
def merchant_info():
    merchant = session.get('merchant', {})
    merchant_id = merchant.get('id')
    if not merchant_id:
        return redirect(url_for('merchant_login'))
    shop = db.session.execute(text('SELECT * FROM shop_info WHERE merchant_id=:merchant_id'), {'merchant_id': merchant_id}).fetchone()
    status = None
    shop_dict = None
    if shop:
        status = shop.status if hasattr(shop, 'status') else shop.get('status', 'nsave')
        shop_dict = dict(shop._mapping)
        # 补全所有前端需要的字段，None转为''
        for k in ['name','category','price_range','description','address','city','district','phone','email','website','wechat','holiday_info']:
            if k not in shop_dict or shop_dict[k] is None:
                shop_dict[k] = ''
        # 兼容前端字段名
        shop_dict['priceRange'] = shop_dict['price_range']
        shop_dict['holidayInfo'] = shop_dict['holiday_info']
        shop_dict['business_hours'] = json.loads(shop_dict.get('business_hours','[]'))
        shop_dict['service_items'] = json.loads(shop_dict.get('service_items','[]'))
        images_raw = shop_dict.get('images', '[]')
        if not images_raw or images_raw.strip() in ['', 'null', 'None']:
            shop_dict['images'] = []
        else:
            shop_dict['images'] = json.loads(images_raw)
    if request.method == 'POST':
        data = request.get_json()
        action = data.get('action', 'save')
        # 必填项校验
        basic = data.get('basicInfo', {})
        location = data.get('locationInfo', {})
        contact = data.get('contactInfo', {})
        required_fields = [
            basic.get('name',''), basic.get('category',''), basic.get('priceRange',''), basic.get('description',''),
            location.get('address',''), location.get('city',''), location.get('district',''),
            contact.get('phone','')
        ]
        if not all(required_fields):
            return jsonify({'success': False, 'message': '请填写所有必填项'})
        business_hours = json.dumps(data.get('businessHours', []), ensure_ascii=False)
        service_items = json.dumps(data.get('serviceItems', []), ensure_ascii=False)
        holiday_info = data.get('holidayInfo', '')
        images = json.dumps(data.get('images', []), ensure_ascii=False) if 'images' in data else ''
        status_val = 'save_npush' if action == 'save' else 'save_push'
        if shop and status in ['save_push', 'formal']:
            return jsonify({'success': False, 'message': '信息已提交或审核通过，无法修改'})
        if shop and status == 'save_npush':
            # 更新
            db.session.execute(text('''
                UPDATE shop_info SET name=:name, category=:category, price_range=:price_range, description=:description, address=:address, city=:city, district=:district, phone=:phone, email=:email, website=:website, wechat=:wechat, holiday_info=:holiday_info, images=:images, business_hours=:business_hours, service_items=:service_items, status=:status WHERE merchant_id=:merchant_id
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
                'service_items': service_items,
                'status': status_val
            })
        else:
            # 新增
            db.session.execute(text('''
                INSERT INTO shop_info (merchant_id, name, category, price_range, description, address, city, district, phone, email, website, wechat, holiday_info, images, business_hours, service_items, status)
                VALUES (:merchant_id, :name, :category, :price_range, :description, :address, :city, :district, :phone, :email, :website, :wechat, :holiday_info, :images, :business_hours, :service_items, :status)
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
                'service_items': service_items,
                'status': status_val
            })
        db.session.commit()
        return jsonify({'success': True, 'message': '店铺信息已保存'})
    # GET请求
    if shop and status == 'save_npush':
        print('shop_info:', shop_dict)  # 打印后端传入的信息
        return render_template('merchant_info_upload.html', shop_info=shop_dict, filled=False, editable=True, status=status)
    elif shop and status in ['save_push', 'formal']:
        print('shop_info:', shop_dict)  # 打印后端传入的信息
        return render_template('merchant_info_upload.html', shop_info=shop_dict, filled=True, editable=False, status=status)
    else:
        print('shop_info: None')  # 打印后端传入的信息
        return render_template('merchant_info_upload.html', shop_info=None, filled=False, editable=True, status='nsave')

@merchant_info_bp.route('/merchant/info/data', methods=['GET'])
def merchant_info_data():
    merchant = session.get('merchant', {})
    merchant_id = merchant.get('id')
    if not merchant_id:
        return jsonify({'success': False, 'data': None})
    shop = db.session.execute(text('SELECT * FROM shop_info WHERE merchant_id=:merchant_id'), {'merchant_id': merchant_id}).fetchone()
    shop_dict = None
    if shop:
        shop_dict = dict(shop._mapping)
        for k in ['name','category','price_range','description','address','city','district','phone','email','website','wechat','holiday_info']:
            if k not in shop_dict or shop_dict[k] is None:
                shop_dict[k] = ''
        shop_dict['priceRange'] = shop_dict['price_range']
        shop_dict['holidayInfo'] = shop_dict['holiday_info']
        shop_dict['business_hours'] = json.loads(shop_dict.get('business_hours','[]'))
        shop_dict['service_items'] = json.loads(shop_dict.get('service_items','[]'))
        images_raw = shop_dict.get('images', '[]')
        if not images_raw or images_raw.strip() in ['', 'null', 'None']:
            shop_dict['images'] = []
        else:
            shop_dict['images'] = json.loads(images_raw)
    return jsonify({'success': True, 'data': shop_dict})
