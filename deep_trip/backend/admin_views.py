from flask import Blueprint, render_template, request, redirect, url_for, flash

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        # TODO: 管理员登录逻辑
        flash('模拟管理员登录成功', 'success')
        return redirect(url_for('admin.admin_dashboard'))
    return render_template('admin_login.html')

@admin_bp.route('/admin/dashboard')
def admin_dashboard():
    return render_template('admin_dashboard.html')

@admin_bp.route('/admin/merchant/review')
def admin_merchant_review():
    return render_template('admin_merchant_review.html')

@admin_bp.route('/admin/data/report')
def admin_data_report():
    return render_template('admin_data_report.html')
