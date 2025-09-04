from flask import Blueprint, render_template, request, redirect, url_for, flash

merchant_bp = Blueprint('merchant', __name__)

@merchant_bp.route('/merchant/login', methods=['GET', 'POST'])
def merchant_login():
    if request.method == 'POST':
        # TODO: 校验商户登录
        flash('模拟商户登录成功', 'success')
        return redirect(url_for('merchant.merchant_login'))
    return render_template('merchant_login.html')

@merchant_bp.route('/merchant/register', methods=['GET', 'POST'])
def merchant_register():
    if request.method == 'POST':
        # TODO: 商户注册逻辑
        flash('模拟商户注册成功', 'success')
        return redirect(url_for('merchant.merchant_login'))
    return render_template('merchant_register.html')

@merchant_bp.route('/merchant/info/upload')
def merchant_info_upload():
    return render_template('merchant_info_upload.html')

@merchant_bp.route('/merchant/feedback')
def merchant_feedback():
    return render_template('merchant_feedback.html')
