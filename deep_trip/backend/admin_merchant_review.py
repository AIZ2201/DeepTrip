from flask import Blueprint, render_template, request, jsonify
from models import db, Merchant, ShopInfo
from sqlalchemy import or_

admin_merchant_review_bp = Blueprint('admin_merchant_review', __name__)

@admin_merchant_review_bp.route('/admin/merchant/review')
def admin_merchant_review():
    return render_template('admin_merchant_review.html')

@admin_merchant_review_bp.route('/admin/merchant/list', methods=['GET'])
def merchant_list():
    status = request.args.get('status', 'all')
    category = request.args.get('category', 'all')
    page = int(request.args.get('page', 1))
    page_size = int(request.args.get('page_size', 10))

    query = db.session.query(ShopInfo, Merchant).join(Merchant, ShopInfo.merchant_id == Merchant.id)

    # 状态映射
    status_map = {
        'pending': 'save_push',
        'approved': 'formal',
        'rejected': 'save_npush',
        'all': None
    }
    db_status = status_map.get(status, None)
    if db_status:
        query = query.filter(ShopInfo.status == db_status)
    if category != 'all':
        query = query.filter(ShopInfo.category == category)

    total = query.count()
    results = query.order_by(ShopInfo.id.desc()).offset((page-1)*page_size).limit(page_size).all()

    merchants = []
    for shop, merchant in results:
        merchants.append({
            'shop_id': shop.id,
            'merchant_id': merchant.id,
            'shop_name': shop.name,
            'category': shop.category,
            'merchant_username': merchant.username,
            'phone': merchant.phone,
            'email': merchant.email,
            'status': shop.status
        })
    return jsonify({'total': total, 'merchants': merchants})

@admin_merchant_review_bp.route('/admin/merchant/detail/<int:shop_id>', methods=['GET'])
def merchant_detail(shop_id):
    shop = ShopInfo.query.get(shop_id)
    if not shop:
        return jsonify({'success': False, 'message': '店铺不存在'})
    merchant = Merchant.query.get(shop.merchant_id)
    if not merchant:
        return jsonify({'success': False, 'message': '商户不存在'})
    # 查询该商户所有 shop_info 记录
    all_shops = ShopInfo.query.filter_by(merchant_id=merchant.id).order_by(ShopInfo.id.desc()).all()
    all_shop_data = [{c.name: getattr(s, c.name) for c in ShopInfo.__table__.columns} for s in all_shops]
    merchant_data = {
        'id': merchant.id,
        'username': merchant.username,
        'phone': merchant.phone,
        'email': merchant.email
    }
    return jsonify({
        'success': True,
        'shop': {c.name: getattr(shop, c.name) for c in ShopInfo.__table__.columns},
        'merchant': merchant_data,
        'all_shop_info': all_shop_data
    })

@admin_merchant_review_bp.route('/admin/merchant/approve', methods=['POST'])
def merchant_approve():
    shop_id = request.form.get('shop_id')
    shop = ShopInfo.query.get(shop_id)
    if not shop:
        return jsonify({'success': False, 'message': '店铺不存在'})
    shop.status = 'formal'
    db.session.commit()
    return jsonify({'success': True, 'message': '已通过审核'})

@admin_merchant_review_bp.route('/admin/merchant/reject', methods=['POST'])
def merchant_reject():
    shop_id = request.form.get('shop_id')
    shop = ShopInfo.query.get(shop_id)
    if not shop:
        return jsonify({'success': False, 'message': '店铺不存在'})
    shop.status = 'save_npush'
    db.session.commit()
    return jsonify({'success': True, 'message': '已拒绝'})