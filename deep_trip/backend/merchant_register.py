import pymysql
from flask import Blueprint, request, jsonify

merchant_register_bp = Blueprint('merchant_register', __name__)

DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '123456',
    'db': 'deeptrip',
    'charset': 'utf8mb4',
    'cursorclass': pymysql.cursors.DictCursor
}

def get_db_connection():
    try:
        return pymysql.connect(**DB_CONFIG)
    except Exception as e:
        print(f"[MerchantRegister] 数据库连接失败: {e}")
        return None

@merchant_register_bp.route('/merchant/register', methods=['POST'])
def merchant_register():
    username = request.form.get('username', '').strip()
    email = request.form.get('email', '').strip()
    phone = request.form.get('phone', '').strip()
    password = request.form.get('password', '').strip()
    business_type = request.form.get('business_type', '').strip()

    print('DEBUG 注册参数:', {
        'username': username,
        'email': email,
        'phone': phone,
        'password': password,
        'business_type': business_type
    })  # 打印所有参数

    # 基本校验
    if not username or not email or not phone or not password or not business_type:
        print('DEBUG 校验失败:', {
            'username': username,
            'email': email,
            'phone': phone,
            'password': password,
            'business_type': business_type
        })  # 校验失败时也打印
        return jsonify({'success': False, 'message': '请填写所有必填项'})

    conn = get_db_connection()
    if not conn:
        return jsonify({'success': False, 'message': '数据库连接失败，请稍后重试'})

    try:
        with conn.cursor() as cursor:
            # 查重
            cursor.execute("SELECT id FROM merchant_login WHERE username=%s OR email=%s OR phone=%s", (username, email, phone))
            if cursor.fetchone():
                return jsonify({'success': False, 'message': '用户名/邮箱/手机号已被注册'})

            # 插入（去掉 name 字段）
            cursor.execute("""
                INSERT INTO merchant_login (username, email, phone, password, business_type, status)
                VALUES (%s, %s, %s, %s, %s, 'pending')
            """, (username, email, phone, password, business_type))
            conn.commit()
            return jsonify({'success': True, 'message': '注册成功，待审核'})
    except pymysql.MySQLError as e:
        conn.rollback()
        print(f"[MerchantRegister] 数据库操作失败: {e}")
        return jsonify({'success': False, 'message': '注册失败，请稍后重试'})
    finally:
        conn.close()